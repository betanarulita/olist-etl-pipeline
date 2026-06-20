import sqlite3
import pandas as pd

DB_PATH = "output/olist.db"

def run_query(conn, title, query):
    print(f"\n{'='*50}")
    print(f"📊 {title}")
    print('='*50)
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))
    return df

def analyze():
    conn = sqlite3.connect(DB_PATH)

    # ── 1. Revenue by order status ─────────────────
    # Pertanyaan: berapa revenue yang hilang dari cancelled order?
    run_query(conn, "Revenue by Order Status", """
        SELECT 
            order_status,
            COUNT(DISTINCT order_id)        AS total_orders,
            ROUND(SUM(payment_value), 2)    AS total_revenue,
            ROUND(AVG(payment_value), 2)    AS avg_revenue
        FROM tbl_master
        GROUP BY order_status
        ORDER BY total_revenue DESC
    """)

    # ── 2. Late delivery analysis ───────────────────
    # Pertanyaan: berapa % order terlambat dan impact revenue-nya?
    run_query(conn, "Late Delivery Impact", """
        SELECT
            is_late,
            COUNT(DISTINCT order_id)        AS total_orders,
            ROUND(SUM(payment_value), 2)    AS total_revenue,
            ROUND(AVG(payment_value), 2)    AS avg_order_value
        FROM tbl_master
        GROUP BY is_late
        ORDER BY is_late
    """)

    # ── 3. Top 10 category by revenue ──────────────
    # Pertanyaan: kategori produk mana yang generate revenue terbesar?
    run_query(conn, "Top 10 Category by Revenue", """
        SELECT
            product_category_name_english   AS category,
            COUNT(DISTINCT order_id)        AS total_orders,
            ROUND(SUM(payment_value), 2)    AS total_revenue,
            ROUND(AVG(payment_value), 2)    AS avg_order_value
        FROM tbl_master
        WHERE order_status != 'canceled'
        AND product_category_name_english IS NOT NULL
        GROUP BY category
        ORDER BY total_revenue DESC
        LIMIT 10
    """)

    # ── 4. Cancelled orders by category ────────────
    # Pertanyaan: kategori mana yang paling banyak dibatalkan?
    run_query(conn, "Cancelled Orders by Category", """
        SELECT
            product_category_name_english   AS category,
            COUNT(DISTINCT order_id)        AS cancelled_orders,
            ROUND(SUM(payment_value), 2)    AS revenue_lost
        FROM tbl_master
        WHERE order_status = 'canceled'
        GROUP BY category
        ORDER BY cancelled_orders DESC
        LIMIT 10
    """)

    # ── 5. Monthly revenue trend ────────────────────
    # Pertanyaan: bagaimana tren revenue per bulan?
    run_query(conn, "Monthly Revenue Trend", """
        SELECT
            strftime('%Y-%m', order_purchase_timestamp) AS month,
            COUNT(DISTINCT order_id)                    AS total_orders,
            ROUND(SUM(payment_value), 2)                AS total_revenue
        FROM tbl_master
        WHERE order_status != 'canceled'
        AND order_purchase_timestamp IS NOT NULL
        GROUP BY month
        ORDER BY month
    """)

    conn.close()
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    analyze()