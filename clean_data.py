import pandas as pd
import os

os.makedirs("cleaned", exist_ok=True)

# ── Load raw data ──
orders = pd.read_csv("olist_orders_dataset.csv")
items = pd.read_csv("olist_order_items_dataset.csv")
customers = pd.read_csv("olist_customers_dataset.csv")
products = pd.read_csv("olist_products_dataset.csv")
payments = pd.read_csv("olist_order_payments_dataset.csv")
reviews = pd.read_csv("olist_order_reviews_dataset.csv")
sellers = pd.read_csv("olist_sellers_dataset.csv")
geo = pd.read_csv("olist_geolocation_dataset.csv")
translation = pd.read_csv("product_category_name_translation.csv")

print("✅ All files loaded")

# ══════════════════════════════════════════════════
# 1. ORDERS — date conversion, drop undelivered
# ══════════════════════════════════════════════════
date_cols = [
    "order_purchase_timestamp", "order_approved_at",
    "order_delivered_carrier_date", "order_delivered_customer_date",
    "order_estimated_delivery_date"
]
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col])

orders["order_year"] = orders["order_purchase_timestamp"].dt.year
orders["order_month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)
orders["order_day_of_week"] = orders["order_purchase_timestamp"].dt.day_name()

# Delivery delay in days (actual - estimated)
delivered = orders["order_status"] == "delivered"
orders.loc[delivered, "delivery_delay_days"] = (
    orders.loc[delivered, "order_delivered_customer_date"]
    - orders.loc[delivered, "order_estimated_delivery_date"]
).dt.days
orders.loc[delivered, "actual_delivery_days"] = (
    orders.loc[delivered, "order_delivered_customer_date"]
    - orders.loc[delivered, "order_purchase_timestamp"]
).dt.days
orders["is_late"] = orders["delivery_delay_days"].apply(lambda x: 1 if x and x > 0 else 0)

print(f"✅ Orders cleaned: {orders.shape[0]} rows, nulls filled, dates converted")

# ══════════════════════════════════════════════════
# 2. PRODUCTS — translate category names, fill nulls
# ══════════════════════════════════════════════════
products = products.merge(translation, on="product_category_name", how="left")
products["product_category_name_english"].fillna("other", inplace=True)
products.rename(columns={"product_category_name_english": "category"}, inplace=True)

num_cols = ["product_name_lenght", "product_description_lenght", "product_photos_qty",
            "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]
for col in num_cols:
    products[col].fillna(products[col].median(), inplace=True)

print(f"✅ Products cleaned: {products.shape[0]} rows, categories translated to English")

# ══════════════════════════════════════════════════
# 3. REVIEWS — fill missing text, convert dates
# ══════════════════════════════════════════════════
reviews["review_comment_title"].fillna("", inplace=True)
reviews["review_comment_message"].fillna("", inplace=True)
reviews["review_creation_date"] = pd.to_datetime(reviews["review_creation_date"])
reviews["review_answer_timestamp"] = pd.to_datetime(reviews["review_answer_timestamp"])

print(f"✅ Reviews cleaned: {reviews.shape[0]} rows, {reviews['review_comment_message'].eq('').sum()} empty messages filled")

# ══════════════════════════════════════════════════
# 4. CUSTOMERS — standardize city names
# ══════════════════════════════════════════════════
customers["customer_city"] = customers["customer_city"].str.strip().str.title()
sellers["seller_city"] = sellers["seller_city"].str.strip().str.title()

print(f"✅ Customers cleaned: {customers.shape[0]} rows")

# ══════════════════════════════════════════════════
# 5. GEOLOCATION — deduplicate (keep first per zip)
# ══════════════════════════════════════════════════
geo_dedup = geo.drop_duplicates(subset="geolocation_zip_code_prefix", keep="first")
print(f"✅ Geolocation deduped: {geo.shape[0]} → {geo_dedup.shape[0]} rows")

# ══════════════════════════════════════════════════
# 6. ITEMS — convert shipping_limit_date
# ══════════════════════════════════════════════════
items["shipping_limit_date"] = pd.to_datetime(items["shipping_limit_date"])
items["total_price"] = items["price"] + items["freight_value"]

print(f"✅ Items cleaned: {items.shape[0]} rows, total_price added")

# ══════════════════════════════════════════════════
# 7. PAYMENTS — aggregate per order
# ══════════════════════════════════════════════════
payments_agg = payments.groupby("order_id").agg(
    total_payment=("payment_value", "sum"),
    payment_installments=("payment_installments", "max"),
    payment_type=("payment_type", "first")
).reset_index()

print(f"✅ Payments aggregated: {payments.shape[0]} → {payments_agg.shape[0]} per order")

# ══════════════════════════════════════════════════
# BUILD MASTER TABLE for Power BI
# ══════════════════════════════════════════════════
master = orders.merge(customers, on="customer_id", how="left")
master = master.merge(items, on="order_id", how="left")
master = master.merge(products[["product_id", "category", "product_weight_g"]], on="product_id", how="left")
master = master.merge(payments_agg, on="order_id", how="left")
master = master.merge(reviews[["order_id", "review_score", "review_comment_message"]], on="order_id", how="left")

print(f"\n✅ Master table built: {master.shape[0]} rows × {master.shape[1]} columns")

# ══════════════════════════════════════════════════
# RFM TABLE
# ══════════════════════════════════════════════════
snapshot_date = orders["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

rfm = orders[orders["order_status"] == "delivered"].merge(items, on="order_id", how="left")
rfm = rfm.merge(customers[["customer_id", "customer_unique_id"]], on="customer_id", how="left")

rfm_table = rfm.groupby("customer_unique_id").agg(
    recency=("order_purchase_timestamp", lambda x: (snapshot_date - x.max()).days),
    frequency=("order_id", "nunique"),
    monetary=("total_price", "sum")
).reset_index()

rfm_table["r_score"] = pd.qcut(rfm_table["recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm_table["f_score"] = pd.qcut(rfm_table["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm_table["m_score"] = pd.qcut(rfm_table["monetary"], 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm_table["rfm_score"] = rfm_table["r_score"] + rfm_table["f_score"] + rfm_table["m_score"]

def segment(row):
    if row["rfm_score"] >= 12:
        return "Champion"
    elif row["rfm_score"] >= 9:
        return "Loyal"
    elif row["rfm_score"] >= 6:
        return "At Risk"
    else:
        return "Lost"

rfm_table["segment"] = rfm_table.apply(segment, axis=1)

print(f"✅ RFM table built: {rfm_table.shape[0]} customers")
print(f"   Segments: {rfm_table['segment'].value_counts().to_dict()}")

# ══════════════════════════════════════════════════
# CHURN TABLE
# ══════════════════════════════════════════════════
churn = orders[orders["order_status"] == "delivered"].merge(
    customers[["customer_id", "customer_unique_id", "customer_city", "customer_state"]],
    on="customer_id", how="left"
)
churn_table = churn.groupby("customer_unique_id").agg(
    last_order_date=("order_purchase_timestamp", "max"),
    total_orders=("order_id", "nunique"),
    customer_city=("customer_city", "first"),
    customer_state=("customer_state", "first")
).reset_index()

churn_table["days_since_last_order"] = (snapshot_date - churn_table["last_order_date"]).dt.days
churn_table["is_churned"] = (churn_table["days_since_last_order"] > 90).astype(int)
churn_table["churn_label"] = churn_table["is_churned"].map({1: "Churned", 0: "Active"})

print(f"✅ Churn table built: {churn_table.shape[0]} customers")
print(f"   Churn rate: {churn_table['is_churned'].mean():.1%}")

# ══════════════════════════════════════════════════
# EXPORT ALL CLEANED FILES
# ══════════════════════════════════════════════════
master.to_csv("cleaned/master_orders.csv", index=False)
rfm_table.to_csv("cleaned/rfm_customers.csv", index=False)
churn_table.to_csv("cleaned/churn_customers.csv", index=False)
orders.to_csv("cleaned/orders_cleaned.csv", index=False)
products.to_csv("cleaned/products_cleaned.csv", index=False)
reviews.to_csv("cleaned/reviews_cleaned.csv", index=False)
customers.to_csv("cleaned/customers_cleaned.csv", index=False)
sellers.to_csv("cleaned/sellers_cleaned.csv", index=False)
geo_dedup.to_csv("cleaned/geolocation_cleaned.csv", index=False)
items.to_csv("cleaned/items_cleaned.csv", index=False)
payments_agg.to_csv("cleaned/payments_cleaned.csv", index=False)

print("\n" + "="*50)
print("🎯 ALL CLEANED FILES EXPORTED TO 'cleaned/' FOLDER:")
print("="*50)
for f in sorted(os.listdir("cleaned")):
    size = os.path.getsize(f"cleaned/{f}") / (1024*1024)
    print(f"  📁 cleaned/{f} ({size:.1f} MB)")

print("\n📊 FILES → POWER BI DASHBOARD MAPPING:")
print("  Dashboard 1 (Sales):     master_orders.csv")
print("  Dashboard 2 (Churn):     churn_customers.csv")
print("  Dashboard 3 (RFM):       rfm_customers.csv")
print("  Dashboard 4 (Delivery):  master_orders.csv (has delay cols)")
print("  Dashboard 5 (Reviews):   master_orders.csv + reviews_cleaned.csv")
