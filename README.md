# tiny-chess-01 — 4 KB chess engine

A chess engine in ≤ 4,096 bytes of Python (stdlib only), for the make.fun
bounty "tiny-chess-01": build the strongest chess engine in 4 KB of Python.

## Files

- `LICENSE` — MIT license
- `README.md` — this file
- `main.py` — the engine (4,096 bytes as committed)
- `.makefun/owner.json` — claim file naming the entrant's wallet

`main.py` is self-contained: it reads, imports, opens or runs no other
file and holds no data outside its own bytes. It speaks the env
protocol (`POST /game {}`, `POST /move {"game": n, "move": "<uci>"}`,
`POST /resign`) using only `urllib` and `json` from the standard
library. Run as `python3 -P -s main.py` with `MAKEFUN_ENV_URL` set.

## Engine (v6)

- 120-char string board (10x12 mailbox), 180-degree rotation flip
  after each move, so the search always sees "white to move".
- Move generation: data-driven direction tables; full rules — castling
  (with attacked-square checks), en passant, promotion. King captures
  are excluded (illegal).
- Search: negamax + alpha-beta, iterative deepening, fixed budget of
  50,000 nodes/move (deterministic: no wall clock, no unseeded
  randomness). Quiescence merged into the main search (captures and
  promotions at depth ≤ 0; all replies when in check). Check
  extensions (depth +1 in check). Transposition table stores the best
  move for ordering only. MVV-LVA capture ordering, TT-move ordering
  at the root. The root skips moves that leave its own king in check.
- Eval: material (P100 N320 B330 R500 Q900) + piece-square terms
  (centrality for non-pawns, linear pawn bonus), precomputed into a
  lookup table at import. The score is carried incrementally in the
  position tuple (updated on make/unmake, negated on flip), so leaf
  eval is O(1).

## Correctness and results

Perft verified against python-chess on the kit positions: startpos
d1–4 = 20/400/8902/197281, all matching. Incremental eval checked
against full recomputation over random playouts (0 mismatches).
Known limitation: castling is fixed-square, so the engine cannot
castle as black (after the flip the king sits on d1). This costs Elo
as black.

Practice Elo (3 trials): 989 / 1,087 / 1,396, mean 1,157 — clears
the 1,154 entry floor. No illegal moves, no time losses (worst move
~4.6 s, trial walls 846–1,263 s of the 1,800 s limit). Deterministic:
trial 0 run twice gave byte-identical games and the same Elo.

## License

MIT. See LICENSE.
