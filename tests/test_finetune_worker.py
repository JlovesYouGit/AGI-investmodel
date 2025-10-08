"""Tests for the finetune worker module."""

from unittest.mock import patch
from trade_mcp.finetune_worker import FineTuneWorker


def test_finetune_worker_initialization():
    """Test that the FineTuneWorker can be initialized."""
    worker = FineTuneWorker()
    assert isinstance(worker, FineTuneWorker)
    assert worker.last_processed_count == 0
    assert worker.running is False


def test_finetune_worker_start():
    """Test that the FineTuneWorker can start."""
    with patch('threading.Thread') as mock_thread:
        worker = FineTuneWorker()
        worker.start()
        
        assert worker.running is True
        mock_thread.assert_called_once()


def test_finetune_worker_stop():
    """Test that the FineTuneWorker can stop."""
    with patch('threading.Thread'):
        worker = FineTuneWorker()
        worker.start()
        worker.stop()
        
        assert worker.running is False