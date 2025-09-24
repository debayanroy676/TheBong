# TheBong 🐍🇮🇳

**TheBong** is the first ever programming language designed in **Bengali**.  
It allows you to write code using Bengali keywords and types, while keeping numbers and operators in English.  
Under the hood, TheBong transpiles into Python — so you get the full power of the Python ecosystem with the elegance of Bangla syntax.

---

## ✨ Features
- **Bangla Keywords** → Example: `ফাংশন` instead of `def`, `যদি` instead of `if`.  
- **Bangla Data Types** → Mapped to Python / NumPy:
  - `হ` → int16  
  - `ই` → int32  
  - `ঈ` → int64  
  - `ড` → float16  
  - `উ` → float32  
  - `ঊ` → float64  
  - `ঋ` → string  
- **English Numbers** → Use `123`, `3.14`, etc. directly.  
- **Easy Execution** → Transpile `.bong` code into Python and run it.  
- **Interoperability** → Access any Python libraries directly.  

---

## 📦 Installation
```bash
git clone https://github.com/yourusername/TheBong.git
cd TheBong
python thebong_transpiler.py <filename.bong>
python <filename.py>
```
## Working 
the transpiler converts ".bong" files to ".py" which is now executable through python.
