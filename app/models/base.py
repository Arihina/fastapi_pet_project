from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class Order(Base):
    __tablename__ = "Заказ"

    order_id: Mapped[int] = mapped_column("код_заказа", primary_key=True)
    product_quantity: Mapped[int] = mapped_column("количество_товаров")
    total_cost: Mapped[float] = mapped_column("общие_затраты")
    supplier_id: Mapped[int] = mapped_column("код_поставщика")
