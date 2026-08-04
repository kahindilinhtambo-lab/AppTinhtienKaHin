import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Order Nhà Hàng", layout="wide")

# ==========================
# Khởi tạo Session State
# ==========================
if "orders" not in st.session_state:
    # orders = {
    #   "Bàn 1":{
    #        "Pizza":{...},
    #        "Coca":{...}
    #   }
    # }
    st.session_state.orders = {}

if "history" not in st.session_state:
    # Lưu hóa đơn đã thanh toán
    st.session_state.history = []

# ==========================
# Thực đơn
# ==========================
menu = {
    "Đồ ăn": {
        "Pizza Hải Sản": 150000,
        "Mì Ý Bò Bằm": 95000,
        "Burger Gà": 65000,
        "Salad Trộn": 50000,
        "Bít tết Bò Mỹ": 250000,
        "Sườn nướng BBQ": 180000,
        "Cánh gà chiên mắm": 75000,
        "Lẩu cá diêu hồng": 200000,
        "Lẩu Thái hải sản": 300000
    },
    "Thức uống": {
        "Coca Cola": 20000,
        "Trà Đào Cam Sả": 35000,
        "Cà Phê Sữa": 25000,
        "Nước Suối": 10000,
        "Sinh tố Bơ": 45000,
        "Nước ép cam": 40000,
        "Mojito chanh dây": 55000,
        "Bia Heineken": 30000
    }
}

# ==========================
# Sidebar
# ==========================
st.sidebar.title("MENU")

page = st.sidebar.radio(
    "Chọn chức năng",
    ["Order", "Admin"]
)

# ==========================================================
# TRANG ORDER
# ==========================================================
if page == "Order":

    st.title("🍽️ Hệ thống Order Nhà Hàng _ Ka Hin")
    st.subheader("Ka Hin Restaurant & More")

    table = st.number_input(
        "Nhập số bàn",
        min_value=1,
        max_value=100,
        step=1
    )

    table_name = f"Bàn {table}"

    if table_name not in st.session_state.orders:
        st.session_state.orders[table_name] = {}

    order_dict = st.session_state.orders[table_name]

    col1, col2 = st.columns([1, 1.5])

    # ======================
    # Chọn món
    # ======================
    with col1:

        st.subheader("Chọn món")

        category = st.selectbox(
            "Loại",
            list(menu.keys())
        )

        item = st.selectbox(
            "Món",
            list(menu[category].keys())
        )

        quantity = st.number_input(
            "Số lượng",
            min_value=1,
            value=1
        )

        if st.button("➕ Thêm vào giỏ"):

            price = menu[category][item]

            if item in order_dict:

                order_dict[item]["Số lượng"] += quantity

                order_dict[item]["Thành tiền"] = (
                        order_dict[item]["Số lượng"] * price
                )

            else:

                order_dict[item] = {
                    "Tên món": item,
                    "Đơn giá": price,
                    "Số lượng": quantity,
                    "Thành tiền": price * quantity
                }

            st.success(f"Đã thêm {item}")

    # ======================
    # Giỏ hàng
    # ======================
    with col2:

        st.subheader(f"🛒 Giỏ hàng - {table_name}")

        if order_dict:

            df = pd.DataFrame.from_dict(
                order_dict,
                orient="index"
            )

            st.table(df[
                ["Tên món", "Đơn giá", "Số lượng", "Thành tiền"]
            ])

            tam_tinh = df["Thành tiền"].sum()

            # Giảm giá 5% nếu hóa đơn trên 1 triệu
            giam_gia = 0

            if tam_tinh > 1000000:
                giam_gia = tam_tinh * 0.05


            # Sau giảm giá
            thanh_tien = tam_tinh - giam_gia


            # VAT 8%
            vat = thanh_tien * 0.08


            # Tổng thanh toán
            tong = thanh_tien + vat


            st.write(
                f"**Tạm tính:** {tam_tinh:,.0f} VNĐ"
            )


            if giam_gia > 0:
                st.write(
                    f"**Giảm giá (5%):** -{giam_gia:,.0f} VNĐ"
                )


            st.write(
                f"**Sau giảm giá:** {thanh_tien:,.0f} VNĐ"
            )


            st.write(
                f"**Thuế VAT (8%):** +{vat:,.0f} VNĐ"
            )


            st.metric(
                "💰 Tổng thanh toán",
                f"{tong:,.0f} VNĐ"
            )


            colA, colB = st.columns(2)


            # ==========================
            # Nút thanh toán
            # ==========================
            with colA:

                if st.button("💰 Thanh toán"):

                    hoa_don = {
                        "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "Bàn": table_name,
                        "Số món": int(df["Số lượng"].sum()),
                        "Tạm tính": tam_tinh,
                        "Giảm giá": giam_gia,
                        "Sau giảm giá": thanh_tien,
                        "VAT 8%": vat,
                        "Thanh toán": tong
                    }


                    st.session_state.history.append(
                        hoa_don
                    )


                    st.session_state.orders[table_name] = {}


                    st.success(
                        "Thanh toán thành công!"
                    )


                    st.rerun()


            # ==========================
            # Nút xóa giỏ hàng
            # ==========================
            with colB:

                if st.button("🗑️ Xóa giỏ hàng"):

                    st.session_state.orders[table_name] = {}

                    st.success(
                        "Đã xóa giỏ hàng"
                    )

                    st.rerun()
# ==========================================================
# TRANG ADMIN
# ==========================================================
else:

    st.title("👨‍💼 ADMIN")

    st.subheader("Lịch sử hóa đơn")

    if len(st.session_state.history) == 0:

        st.info("Chưa có hóa đơn nào.")

    else:

        history_df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            history_df,
            use_container_width=True
        )

        doanh_thu = history_df["Thanh toán"].sum()

        st.metric(
            "💵 Tổng doanh thu",
            f"{doanh_thu:,.0f} VNĐ"
        )

        st.subheader("Doanh thu theo bàn")

        revenue_table = history_df.groupby("Bàn")[
            "Thanh toán"
        ].sum().reset_index()

        st.dataframe(
            revenue_table,
            use_container_width=True
        )

        if st.button("🗑️ Xóa toàn bộ lịch sử"):

            st.session_state.history = []

            st.success("Đã xóa toàn bộ dữ liệu.")

            st.rerun()
