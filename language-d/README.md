# language-d

さまざまなプログラミング言語で「1~10の中で、偶数の2乗の合計」を計算

## 各ファイルについて

- `Elixir.ex` : Elixirによる実装例
- `julia.jl` : Juliaによる実装例
- `lua.lua` : Luaによる実装例
- `rust.rs` : Rustによる実装例
- `nim.nim` : Nimによる実装例
- `haskell.hs` : Haskellによる実装例
- `ocaml.ml` : OCamlによる実装例
- `crystal.cr` : Crystalによる実装例
- `fsharp.fsx` : F#による実装例
- `erlang.erl` : Erlangによる実装例
- `scala.scala` : Scalaによる実装例
- `zig.zig` : Zigによる実装例

## 実行方法

各言語の実行環境が必要です。

### Elixir

```sh
elixir Elixir.ex
```

### Julia

```sh
julia julia.jl
```

### Lua

```sh
lua lua.lua
```

### Rust

Rustはコンパイルが必要です。

```sh
rustc rust.rs
./rust
```

### Nim

```sh
nim compile --run nim.nim
```

### Haskell

```sh
runghc haskell.hs
```

### OCaml

```sh
ocaml ocaml.ml
```

### Crystal

```sh
crystal run crystal.cr
```

### F#

```sh
fsharpi fsharp.fsx
```

### Erlang

```sh
erlc erlang.erl
erl -noshell -s erlang main -s init stop
```

### Scala

```sh
scala scala.scala
```

### Zig

```sh
zig run zig.zig
```
