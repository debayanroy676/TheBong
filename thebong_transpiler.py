import re
import sys
from pathlib import Path

# Bengali → Python keyword mappings
KEYWORDS = {
    "পদ্ধতি": "def",
    "যদি": "if",
    "নাহলে": "else",
    "যখন": "while",
    "ফেরত": "return",
    "দেখাও": "print",
    "সত্য": "True",
    "মিথ্যা": "False",
}

# Bengali → Python type mappings
TYPES = {
    "হ": "np.int16",
    "ই": "np.int32",
    "ঈ": "np.int64",
    "ড": "np.float16",
    "উ": "np.float32",
    "ঊ": "np.float64",
    "ঋ": "str",
}

# pattern to find Python string literals (triple or single/double quoted)
_STRING_PATTERN = r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"[^"\n]*"|\'[^\'\n]*\')'

def _extract_strings(code: str):
    """Replace string literals with placeholders and return (code_without_strings, list_of_strings)."""
    strings = []
    def _repl(m):
        idx = len(strings)
        strings.append(m.group(0))
        return f"__STR{idx}__"
    code2 = re.sub(_STRING_PATTERN, _repl, code, flags=re.DOTALL)
    return code2, strings

def _restore_strings(code: str, strings):
    for i, s in enumerate(strings):
        code = code.replace(f"__STR{i}__", s)
    return code

def _remove_comments(code: str) -> str:
    # Convert multi-line TheBong comments ?! ... !? into Python triple-quoted strings (preserve content)
    code = re.sub(r"\?!([\s\S]*?)!\?", lambda m: '"""' + m.group(1) + '"""', code, flags=re.DOTALL)
    # Convert single-line comments starting with ??? into Python '# ...'
    code = re.sub(r"\?\?\?([^\n]*)", lambda m: "# " + m.group(1), code)
    return code

def _replace_tokens(code: str) -> str:
    """
    Replace KEYWORDS and TYPES while ensuring we only match whole tokens.
    We consider boundaries to be ASCII letters/digits/underscore and Bengali block \u0980-\u09FF.
    """
    boundary = r"[A-Za-z0-9_\u0980-\u09FF]"
    out = code
    for bn, en in KEYWORDS.items():
        pattern = rf"(?<!{boundary}){re.escape(bn)}(?!{boundary})"
        out = re.sub(pattern, en, out)
    for bn, en in TYPES.items():
        pattern = rf"(?<!{boundary}){re.escape(bn)}(?!{boundary})"
        out = re.sub(pattern, en, out)
    return out

def transpile(bn_code: str) -> str:
    # 1) protect strings
    code_no_strings, strings = _extract_strings(bn_code)

    # 2) remove/transform comments (safe because strings are protected)
    code_no_comments = _remove_comments(code_no_strings)

    # 3) replace tokens (keywords & types)
    py_core = _replace_tokens(code_no_comments)

    # 4) restore strings
    py_core = _restore_strings(py_core, strings)

    # 5) add numpy import automatically if Bengali types are present in the original source
    if any(bn in bn_code for bn in TYPES.keys()):
        py_core = "import numpy as np\n" + py_core

    return py_core

def main():
    if len(sys.argv) < 2:
        print("Usage: python thebong_transpiler.py <file.bong>")
        sys.exit(1)

    path = Path(sys.argv[1])
    bn_code = path.read_text(encoding="utf-8")
    py_code = transpile(bn_code)

    out_path = path.with_suffix(".py")
    out_path.write_text(py_code, encoding="utf-8")

    print(f"✅ Transpiled {path} → {out_path}")

if __name__ == "__main__":
    main()
