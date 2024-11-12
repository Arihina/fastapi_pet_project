import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()


class Order(Base):
    __tablename__ = "Заказ"

    id: Mapped[int] = mapped_column("код_заказа", primary_key=True)
    product_quantity: Mapped[int] = mapped_column("количество_товаров")
    total_cost: Mapped[float] = mapped_column("общие_затраты")
    provider_id: Mapped[int] = mapped_column("код_поставщика")

    provider = relationship('Provider', back_populates='Заказ')
    product = relationship('Product', back_populates='Заказ')


class Description(Base):
    __tablename__ = "Описание"

    id: Mapped[int] = mapped_column("код_описания", primary_key=True)
    furniture_type: Mapped[str] = mapped_column("тип_мебели")
    material: Mapped[str] = mapped_column("материал")
    weight: Mapped[int] = mapped_column("вес")
    dimensions: Mapped[int] = mapped_column("габариты")

    product = relationship('Product', back_populates='Описание')


class Buyer(Base):
    __tablename__ = "Покупатель"

    id: Mapped[int] = mapped_column("код_покупателя", primary_key=True)
    full_name: Mapped[str] = mapped_column("ФИО")
    organization_name: Mapped[str] = mapped_column("имя_организации")
    phone_number: Mapped[str] = mapped_column("телефон")
    address: Mapped[str] = mapped_column("адрес")

    sales_accounting = relationship('SalesAccounting', back_populates='Покупатель')


class Provider(Base):
    __tablename__ = "Поставщик"

    id: Mapped[int] = mapped_column("код_поставщика", primary_key=True)
    full_name: Mapped[str] = mapped_column("ФИО")
    product_name: Mapped[str] = mapped_column("название_товара")
    phone_number: Mapped[str] = mapped_column("телефон")
    email: Mapped[str] = mapped_column("email")

    order = relationship('Order', back_populates='Поставщик')


class Product(Base):
    __tablename__ = "Товар"

    id: Mapped[int] = mapped_column("код_товара", primary_key=True)
    price: Mapped[float] = mapped_column("цена_продажи")
    count: Mapped[int] = mapped_column("количество")
    order_id: Mapped[int] = mapped_column("код_заказа", ForeignKey('Заказ.код_заказа'))
    description_id: Mapped[int] = mapped_column("код_описания")

    order = relationship('Order', back_populates='Товар')
    description = relationship('Description', back_populates='Товар')
    sales_accounting = relationship('SalesAccounting', back_populates='Товар')


class SalesAccounting(Base):
    __tablename__ = "Учёт_продаж"

    id: Mapped[int] = mapped_column("код_продажи", primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column("дата_продажи")
    product_id: Mapped[int] = mapped_column("код_товара")
    buyer_id: Mapped[int] = mapped_column("код_покупателя")

    product = relationship('Product', back_populates='Учёт_продаж')
    buyer = relationship('Buyer', back_populates='Учёт_продаж')
