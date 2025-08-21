# mymodule.py

def public_func():
    return "✅ public function called"

def another_func():
    return "✅ another function called"

def _private_func():
    return "❌ private function called"

# 指定模块公开 API
__all__ = ["public_func"]
