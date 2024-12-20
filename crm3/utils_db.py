import contextlib
from owm.models import Awaiting, Awaiting_product

DATABASE_URL = "postgresql+asyncpg://crm3:Billkill13@postgres:5432/postgres"

# Создаем движок

#engine = create_async_engine(DATABASE_URL, future=True)
# Создаем сессию
#AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Базовый класс для моделей SQLAlchemy
#Base = declarative_base()

'''
@contextlib.asynccontextmanager
async def get_db_session() -> AsyncGenerator:
    """
    Контекстный менеджер для управления сессией базы данных.
    """
    try:
        session = AsyncSessionLocal()
        yield session
    finally:
        await session.close()
        await engine.dispose()

@contextlib.asynccontextmanager
async def get_http_session():
    """
    Контекстный менеджер для управления сессией aiohttp.
    """
    async with aiohttp.ClientSession() as session:
        try:
            yield session
        finally:
            await session.close()
'''

def db_check_awaiting_postingnumber(posting_numbers: list):
    found_records = Awaiting.objects.filter(posting_number__in=posting_numbers)
    found_posting_numbers = set(found_records.values_list('posting_number', flat=True))
    not_found_records = [pn for pn in posting_numbers if pn not in found_posting_numbers]
    result = {'found': found_posting_numbers, 'not_found': not_found_records}
    return result

def db_create_customerorder(not_found_product: dict):
    try:
        for posting_number, products in not_found_product.items():
            # Создаем запись в таблице OwmAwaiting
            awaiting_record = Awaiting.objects.create(
                posting_number=posting_number,
                status=products['status']
                )

            for product in products['product_list']:
                print(f'#' * 40)
                print(f"product {product}")
                print(f'#' * 40)
                # Создаем запись в таблице OwmAwaitingProduct
                Awaiting_product.objects.create(
                    awaiting=awaiting_record,
                    offer_id=product['offer_id'],
                    price=int(float(product['price'])),
                    quantity=product['quantity']
                    )
    except Exception as e:
        # Логируем ошибку или поднимаем исключение, если нужно
        print(f"Error occurred: {e}")
        raise
