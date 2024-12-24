import contextlib
from owm.models import Awaiting, Awaiting_product, Metadata
from typing import Any, Dict

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


def db_get_metadata(seller) -> Dict[str, Any]:
    """
    Извлекает метаданные для указанного продавца (seller) из модели Metadata.

    Для каждой ключевой сущности (organization, ozon, yandex, wb) в meta_mapping
    выполняется запрос Metadata.objects.filter(seller=seller, name=<значение>).
    Если хотя бы одна запись найдена, берётся первый элемент, и его metadata_dict
    сохраняется в результирующем словаре result по соответствующему ключу.

    :param seller: Объект продавца (или идентификатор продавца),
                   для которого необходимо получить метаданные.
    :return: Словарь, где ключи — это названия сущностей
             ('organization', 'ozon', 'yandex', 'wb'), а значения —
             соответствующие метаданные (metadata_dict),
             если запись в БД найдена.
    """

    meta_mapping = {
        'organization': 'ms_organization',
        'ozon': 'ms_ozon_contragent',
        'yandex': 'ms_yandex_contragent',
        'wb': 'ms_wb_contragent',
    }

    result = {}
    for key, meta_name in meta_mapping.items():
        metadata_record = Metadata.objects.filter(seller=seller, name=meta_name).first()
        if metadata_record is not None:
            result[key] = metadata_record.metadata_dict

    return result

def db_update_metadata(seller, metadata) -> Dict[str, Any]:
    """
    обновляем метаданные для указанного продавца (seller)
    """

    meta_mapping = {
        'organization': 'ms_organization',
        'ozon': 'ms_ozon_contragent',
        'yandex': 'ms_yandex_contragent',
        'wb': 'ms_wb_contragent',
    }

    result = {}
    for key, meta_name in meta_mapping.items():
        metadata_record = Metadata.objects.filter(seller=seller, name=meta_name).first()

        if metadata_record is not None:
            result[key] = metadata_record.metadata_dict

    return result

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
