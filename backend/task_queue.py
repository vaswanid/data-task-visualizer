import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any
from fastapi import FastAPI
import threading
import time
import queue
import uuid

queue = asyncio.Queue()