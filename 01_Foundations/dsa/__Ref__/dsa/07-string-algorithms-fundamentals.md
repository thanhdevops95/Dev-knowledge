# 🔤 String Algorithms — Thuật toán xử lý chuỗi

> `[INTERMEDIATE → ADVANCED]` — Prerequisite: `01-dsa-fundamentals.md`
> Pattern matching, text search, và string manipulation cho interviews và production.

---

## Tại sao cần String Algorithms?

Chuỗi (string) xuất hiện **mọi nơi** trong phần mềm: tìm kiếm text trong IDE, grep trong terminal, autocomplete trong search bar, kiểm tra DNA sequences, spam filter email. Biết thuật toán chuỗi hiệu quả giúp xử lý **hàng triệu ký tự** trong milliseconds thay vì seconds.

| Bài toán | Naive | Tối ưu | Thuật toán |
|---|---|---|---|
| Pattern matching | O(n × m) | **O(n + m)** | KMP, Rabin-Karp |
| Multiple patterns | O(n × m × k) | **O(n + Σm)** | Aho-Corasick |
| Autocomplete | O(n × k) | **O(L)** per query | Trie |
| Suffix operations | O(n²) | **O(n)** | Suffix Array |

---

## 1. KMP (Knuth-Morris-Pratt) — O(n + m)

### Vấn đề của Naive Search

```
Text:    "ABABDABACDABABCABAB"
Pattern: "ABABCABAB"

Naive: mỗi lần mismatch, quay lại vị trí tiếp theo → O(n × m)
KMP:   không bao giờ quay lại text → O(n + m)
```

### Failure Function (Prefix Table)

KMP dùng **failure function** để biết khi mismatch, nhảy đến đâu thay vì quay lại đầu pattern.

```python
def compute_lps(pattern: str) -> list[int]:
    """
    LPS (Longest Proper Prefix which is also Suffix).
    lps[i] = length of longest proper prefix of pattern[0..i]
             that is also a suffix.
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # Length of previous longest prefix-suffix
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]  # Don't increment i!
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str) -> list[int]:
    """Find all occurrences of pattern in text — O(n + m)."""
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    
    matches = []
    i = j = 0  # i for text, j for pattern
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            matches.append(i - j)  # Match found!
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]  # Use failure function — skip!
            else:
                i += 1
    
    return matches

print(kmp_search("ABABDABACDABABCABAB", "ABABCABAB"))
# [9] — match at index 9
```

---

## 2. Rabin-Karp — Rolling Hash

**Ý tưởng:** Thay vì so sánh từng ký tự, tính **hash cửa sổ trượt** và so sánh hash. Hash match → verify bằng string compare.

```python
def rabin_karp(text: str, pattern: str) -> list[int]:
    """
    Rolling hash search — O(n + m) average.
    Good for MULTIPLE pattern search.
    """
    n, m = len(text), len(pattern)
    BASE, MOD = 256, 101  # Hash parameters
    
    # Compute hash of pattern and first window
    p_hash = 0
    t_hash = 0
    h = pow(BASE, m - 1, MOD)  # BASE^(m-1) mod MOD
    
    for i in range(m):
        p_hash = (BASE * p_hash + ord(pattern[i])) % MOD
        t_hash = (BASE * t_hash + ord(text[i])) % MOD
    
    matches = []
    for i in range(n - m + 1):
        if p_hash == t_hash:
            # Hash match → verify actual string
            if text[i:i + m] == pattern:
                matches.append(i)
        
        # Rolling hash: remove leftmost, add rightmost
        if i < n - m:
            t_hash = (BASE * (t_hash - ord(text[i]) * h) + 
                      ord(text[i + m])) % MOD
            if t_hash < 0:
                t_hash += MOD
    
    return matches
```

### Khi nào dùng Rabin-Karp vs KMP?

| | KMP | Rabin-Karp |
|---|---|---|
| **Single pattern** | ✅ O(n+m) guaranteed | O(n+m) average |
| **Multiple patterns** | Phải chạy lại mỗi pattern | ✅ Tính hash 1 lần |
| **Worst case** | O(n+m) | O(n×m) (hash collision) |

---

## 3. Z-Algorithm — Z-Array

Z-array: `z[i]` = độ dài chuỗi con bắt đầu tại `i` mà **khớp với prefix** của chuỗi gốc.

```python
def z_function(s: str) -> list[int]:
    """
    z[i] = length of longest substring starting from s[i]
           that matches a prefix of s.
    """
    n = len(s)
    z = [0] * n
    z[0] = n  # Entire string is prefix of itself
    left, right = 0, 0  # Z-box [left, right]
    
    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])
        
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        
        if i + z[i] > right:
            left, right = i, i + z[i]
    
    return z

def z_search(text: str, pattern: str) -> list[int]:
    """Pattern matching using Z-algorithm."""
    combined = pattern + "$" + text  # Sentinel character
    z = z_function(combined)
    m = len(pattern)
    
    return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] == m]

print(z_search("aabxaabaab", "aab"))
# [0, 4, 7]
```

---

## 4. Boyer-Moore — Thực tế nhanh nhất

Boyer-Moore scan pattern **từ phải sang trái** và dùng 2 heuristics để nhảy xa hơn khi mismatch.

```python
def boyer_moore_simple(text: str, pattern: str) -> list[int]:
    """Simplified Boyer-Moore with Bad Character rule only."""
    n, m = len(text), len(pattern)
    
    # Bad character table: last occurrence of each char in pattern
    bad_char = {}
    for i, c in enumerate(pattern):
        bad_char[c] = i
    
    matches = []
    shift = 0
    
    while shift <= n - m:
        j = m - 1  # Start from right end of pattern
        
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
        
        if j < 0:
            matches.append(shift)
            shift += 1
        else:
            # Bad character rule: jump!
            bc = bad_char.get(text[shift + j], -1)
            shift += max(1, j - bc)
    
    return matches
```

**Boyer-Moore** là thuật toán dùng trong `grep`, text editors — nhanh nhất trên thực tế vì **nhảy xa** khi mismatch.

---

## 5. Trie Operations — Prefix Tree

Trie đã được giới thiệu trong bài trees. Ở đây ta đi sâu hơn vào operations.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0  # Number of words with this prefix

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1
        node.is_end = True
    
    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix: str) -> bool:
        return self._find(prefix) is not None
    
    def count_prefix(self, prefix: str) -> int:
        """Count words with given prefix."""
        node = self._find(prefix)
        return node.count if node else 0
    
    def autocomplete(self, prefix: str, limit: int = 5) -> list[str]:
        """Return words starting with prefix."""
        node = self._find(prefix)
        if not node:
            return []
        
        results = []
        self._dfs(node, prefix, results, limit)
        return results
    
    def _find(self, prefix: str):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def _dfs(self, node, current, results, limit):
        if len(results) >= limit:
            return
        if node.is_end:
            results.append(current)
        for char in sorted(node.children):
            self._dfs(node.children[char], current + char, results, limit)

# Autocomplete example
trie = Trie()
for word in ["apple", "app", "application", "banana", "band", "apply"]:
    trie.insert(word)

print(trie.autocomplete("app"))
# ['app', 'apple', 'application', 'apply']
print(trie.count_prefix("app"))  # 4
```

---

## 6. Suffix Array — Construction & Applications

```python
def build_suffix_array(text: str) -> list[int]:
    """Build suffix array — sorted indices of all suffixes."""
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort()
    return [idx for _, idx in suffixes]

text = "banana$"
sa = build_suffix_array(text)
# Suffixes sorted:
# $          → index 6
# a$         → index 5
# ana$       → index 3
# anana$     → index 1
# banana$    → index 0
# na$        → index 4
# nana$      → index 2
print(sa)  # [6, 5, 3, 1, 0, 4, 2]
```

**Ứng dụng:** Tìm substring, longest repeated substring, count distinct substrings.

---

## 7. Anagram Detection — Sliding Window

```python
from collections import Counter

def find_anagrams(s: str, p: str) -> list[int]:
    """
    LeetCode 438 — Find all anagram positions.
    Sliding window + frequency count — O(n).
    """
    if len(p) > len(s):
        return []
    
    p_count = Counter(p)
    window = Counter(s[:len(p)])
    
    result = []
    if window == p_count:
        result.append(0)
    
    for i in range(len(p), len(s)):
        # Add new char
        window[s[i]] += 1
        
        # Remove old char
        old = s[i - len(p)]
        window[old] -= 1
        if window[old] == 0:
            del window[old]
        
        if window == p_count:
            result.append(i - len(p) + 1)
    
    return result

print(find_anagrams("cbaebabacd", "abc"))
# [0, 6] — "cba" at 0, "bac" at 6
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Dùng naive O(nm) trong production | Dùng KMP hoặc built-in (optimized) | Python `in` operator đã dùng Boyer-Moore variant |
| 2 | Rabin-Karp không verify khi hash match | LUÔN verify string khi hash match | Hash collision → false positive |
| 3 | Trie cho dataset nhỏ | Trie chỉ hiệu quả khi nhiều prefix queries | Hash map đủ cho single lookups |
| 4 | Quên handle case sensitivity | Normalize trước khi search | `text.lower()` trước khi matching |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Implement naive pattern matching, đo time vs KMP
- [ ] **Bài 2 (Trung bình):** LeetCode 28 — Find the Index of First Occurrence (KMP)
- [ ] **Bài 3 (Trung bình):** LeetCode 438 — Find All Anagrams in a String
- [ ] **Bài 4 (Khó):** LeetCode 208 — Implement Trie + autocomplete
- [ ] **Bài 5 (Khó):** LeetCode 1032 — Stream of Characters (Aho-Corasick / Trie)

---

## Tài nguyên thêm

- [Visualgo — String Matching](https://visualgo.net/en/suffixarray) — Trực quan KMP, Z-algorithm
- [CP-Algorithms — String Processing](https://cp-algorithms.com/string/) — Chi tiết tất cả thuật toán chuỗi
- [CLRS Chapter 32 — String Matching](https://mitpress.mit.edu/9780262046305/) — Sách giáo khoa
- [Aho-Corasick Algorithm (GeeksforGeeks)](https://www.geeksforgeeks.org/aho-corasick-algorithm-pattern-searching/) — Multi-pattern matching
