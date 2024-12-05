import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()


class Order(Base):
    __tablename__ = "Заказ"

    id: Mapped[int] = mapped_column("код", primary_key=True)
    product_quantity: Mapped[int] = mapped_column("количество_товаров")
    total_cost: Mapped[float] = mapped_column("сумма")  # Corrected column name
    product_id: Mapped[int] = mapped_column("код_товара", ForeignKey("Товар.код"))

    product = relationship("Product", back_populates="orders")


class Description(Base):
    __tablename__ = "Описание"

    id: Mapped[int] = mapped_column("код", primary_key=True)
    furniture_type: Mapped[str] = mapped_column("тип_мебели")
    material: Mapped[str] = mapped_column("материал")
    weight: Mapped[int] = mapped_column("вес")
    dimensions: Mapped[str] = mapped_column("габариты")

    products = relationship("Product", back_populates="description")


class Buyer(Base):
    __tablename__ = "Покупатель"

    id: Mapped[int] = mapped_column("код", primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column("ФИО")
    organization_name: Mapped[str] = mapped_column("имя_организации")
    phone_number: Mapped[str] = mapped_column("телефон")
    address: Mapped[str] = mapped_column("адрес")

    sales_records = relationship("SalesRecord", back_populates="buyer")


class Provider(Base):
    __tablename__ = "Поставщик"

    id: Mapped[int] = mapped_column("код", primary_key=True, autoincrement=True)
    organization_name: Mapped[str] = mapped_column("имя_организации")
    phone_number: Mapped[str] = mapped_column("Телефон")
    email: Mapped[str] = mapped_column("Email")

    products = relationship("Product", back_populates="provider")


class Product(Base):
    __tablename__ = "Товар"

    id: Mapped[int] = mapped_column("код", primary_key=True, autoincrement=True)
    description_id: Mapped[int] = mapped_column("код_описания", ForeignKey("Описание.код"))
    price: Mapped[float] = mapped_column("цена")
    stock: Mapped[int] = mapped_column("количество_в_наличии")
    supplier_id: Mapped[int] = mapped_column("код_поставщика", ForeignKey("Поставщик.код"))

    description = relationship("Description", back_populates="products")
    provider = relationship("Provider", back_populates="products")
    orders = relationship("Order", back_populates="product")
    sales_records = relationship("SalesRecord", back_populates="product")


class SalesRecord(Base):
    __tablename__ = "Учёт_продаж"

    id: Mapped[int] = mapped_column("код", primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = mapped_column("дата")
    order_id: Mapped[int] = mapped_column("код_заказа", ForeignKey("Заказ.код"))
    buyer_id: Mapped[int] = mapped_column("код_покупателя", ForeignKey("Покупатель.код"))

    product = relationship("Product", back_populates="sales_records")
    buyer = relationship("Buyer", back_populates="sales_records")
    order = relationship("Order", back_populates="sales_records")  # Added order relationship


class StockRecord(Base):
    __tablename__ = "Учёт_поставок"

    id: Mapped[int] = mapped_column("код", primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = mapped_column("дата")
    product_id: Mapped[int] = mapped_column("код_товара", ForeignKey("Товар.код"))
    quantity: Mapped[int] = mapped_column("количество")

    product = relationship("Product", back_populates="stock_records")
