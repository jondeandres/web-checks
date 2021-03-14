import asyncio
import pytest


@pytest.fixture
def event_loop():
    yield asyncio.get_event_loop()
