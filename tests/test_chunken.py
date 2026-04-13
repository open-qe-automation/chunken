import os
import sys
import pytest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import (
    generate_chunk_id,
    preprocess_text,
    find_text_files,
    read_config
)


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


class TestGenerateChunkId:
    def test_generate_chunk_id(self):
        chunk_id = generate_chunk_id("test_file.txt", 1)
        assert isinstance(chunk_id, str)
        assert len(chunk_id) > 0


class TestPreprocessText:
    def test_preprocess_removes_dates(self):
        text = "Meeting on 2024-01-15 at the office"
        result = preprocess_text(text)
        assert '2024-01-15' not in result

    def test_preprocess_removes_phone(self):
        text = "Call me at 555-123-4567"
        result = preprocess_text(text)
        assert '555-123-4567' not in result

    def test_preprocess_removes_urls(self):
        text = "Check https://example.com for more"
        result = preprocess_text(text)
        assert 'https://example.com' not in result

    def test_preprocess_removes_page_numbers(self):
        text = "Page 1 of document Page 2"
        result = preprocess_text(text)
        assert 'Page 1' not in result


class TestFindTextFiles:
    def test_find_text_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, 'test.txt')
            with open(test_file, 'w') as f:
                f.write("test content")
            
            files = find_text_files([tmpdir])
            assert len(files) == 1
            assert files[0].endswith('.txt')

    def test_find_text_files_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            files = find_text_files([tmpdir])
            assert len(files) == 0


class TestReadConfig:
    def test_read_config(self):
        config = read_config(os.path.join(os.path.dirname(__file__), '..', 'config.json'))
        assert config is not None
        assert 'input_directories' in config
        assert 'chunk_size' in config


if __name__ == '__main__':
    pytest.main([__file__, '-v'])