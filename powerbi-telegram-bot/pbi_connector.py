import os
import glob
import logging
from typing import Optional

from pyadomd import Pyadomd
import pandas as pd

logger = logging.getLogger(__name__)


def find_pbi_port() -> Optional[int]:
    """
    Находит порт локального Analysis Services, запущенного Power BI Desktop.
    Ищет файл msmdsrv.port.txt в стандартных директориях.
    """
    patterns = [
        os.path.expandvars(
            r"%LOCALAPPDATA%\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces\*\Data\msmdsrv.port.txt"
        ),
        os.path.expandvars(
            r"%LOCALAPPDATA%\Packages\Microsoft.MicrosoftPowerBIDesktop_*\LocalState\AnalysisServicesWorkspaces\*\Data\msmdsrv.port.txt"
        ),
    ]

    for pattern in patterns:
        files = glob.glob(pattern)
        if files:
            # Берём самый свежий файл по времени модификации
            latest = max(files, key=os.path.getmtime)
            try:
                with open(latest, "r", encoding="utf-16-le") as f:
                    port_str = f.read().strip()
                    port = int(port_str.replace("\ufeff", "").strip())
                    logger.info(f"Найден порт Power BI: {port} (файл: {latest})")
                    return port
            except Exception as e:
                logger.warning(f"Не удалось прочитать порт из {latest}: {e}")

    logger.error("Не удалось найти порт Power BI. Убедитесь, что Power BI Desktop открыт.")
    return None


def query_pbi(dax_query: str) -> pd.DataFrame:
    """
    Выполняет DAX-запрос к открытому экземпляру Power BI Desktop.
    """
    port = find_pbi_port()
    if port is None:
        raise ConnectionError(
            "Power BI Desktop не найден. Откройте .pbix файл и попробуйте снова."
        )

    conn_str = f"Provider=MSOLAP;Data Source=localhost:{port};"

    try:
        with Pyadomd(conn_str) as conn:
            with conn.cursor().execute(dax_query) as cur:
                cols = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return pd.DataFrame(rows, columns=cols)
    except Exception as e:
        logger.error(f"Ошибка выполнения DAX-запроса: {e}")
        raise