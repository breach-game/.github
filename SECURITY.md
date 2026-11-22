# Security policy

BREACH is a static website: there is no game server, no account and no database. The game simulates every command inside the player's browser tab and never sends a request to the targets it shows.

## Reporting a vulnerability

Please report privately, through GitHub's form on the repository concerned: **Security > Report a vulnerability**.

- The game, its engine and the pack tooling: [breach-game/breach](https://github.com/breach-game/breach/security/advisories/new)
- The community catalogue, its signature or a published pack: [breach-game/packs](https://github.com/breach-game/packs/security/advisories/new)

Never open a public issue for a security problem. We acknowledge reports within a week and keep you informed until the fix is published.

What the game guarantees and how it protects players is described in [breach/SECURITY.md](https://github.com/breach-game/breach/blob/main/SECURITY.md).

## In scope

- Any way for game content (a mission pack, a catalogue) to reach the real network, run code, or escape the terminal's sanitising.
- Any way to make the game accept an unsigned or tampered community catalogue or pack.
- Leaks of the player's API key, when one is set.
- Weaknesses in the build or publishing workflows.

## Not a vulnerability

The fictional vulnerabilities of NovaMind, the target company in the game, are the point of the game. Finding a flag "too easily" is a gameplay issue: open a normal issue.
