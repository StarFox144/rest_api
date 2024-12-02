from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Базовий клас для моделей
Base = declarative_base()

# Модель користувача
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Зв'язок з замовленнями
    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'

# Модель продукту
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    # Зв'язок з елементами замовлення
    order_items = relationship('OrderItem', back_populates='product')

    def __repr__(self):
        return f'<Product {self.name}>'

# Модель замовлення
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='pending')

    # Зв'язки
    user = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order')

    def __repr__(self):
        return f'<Order {self.id}>'

# Модель елементу замовлення
class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Зв'язки
    order = relationship('Order', back_populates='items')
    product = relationship('Product', back_populates='order_items')

    def __repr__(self):
        return f'<OrderItem {self.id}>'

# Налаштування підключення до бази даних
DATABASE_URL = 'sqlite:///ecommerce.db'  # Можна змінити на інший діалект БД
engine = create_engine(DATABASE_URL, echo=True)

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Створення таблиць
def init_db():
    Base.metadata.create_all(engine)

# Приклад додавання даних
def add_sample_data():
    # Створення користувача
    new_user = User(
        username='john_doe', 
        email='john@example.com', 
        password='securepassword123'
    )
    session.add(new_user)

    # Створення продукту
    new_product = Product(
        name='Смартфон',
        description='Сучасний смартфон з потужною камерою',
        price=599.99,
        stock_quantity=50
    )
    session.add(new_product)

    # Створення замовлення
    new_order = Order(
        user=new_user,
        total_amount=599.99,
        status='completed'
    )
    session.add(new_order)

    # Створення елементу замовлення
    new_order_item = OrderItem(
        order=new_order,
        product=new_product,
        quantity=1,
        subtotal=599.99
    )
    session.add(new_order_item)

    # Збереження змін
    session.commit()

# Приклад запиту
def get_user_orders(username):
    user = session.query(User).filter_by(username=username).first()
    if user:
        return user.orders
    return []

# Головна функція для ініціалізації та демонстрації
def main():
    # Створення таблиць
    init_db()

    # Додавання демо-даних
    add_sample_data()

    # Отримання замовлень користувача
    user_orders = get_user_orders('john_doe')
    for order in user_orders:
        print(f"Замовлення {order.id}: Загальна сума {order.total_amount}")

if __name__ == '__main__':
    main()

# Закриття сесії (важливо робити в кінці роботи)
session.close()
