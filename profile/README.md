<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../brand/svg/breach-wordmark-tagline-dark-bg.svg">
    <img alt="BREACH · HACK · DETECT · LEARN" src="../brand/svg/breach-wordmark-tagline-light-bg.svg" width="460">
  </picture>
</p>

<p align="center"><b>A cybersecurity thriller in your browser. Attack, understand, then defend.</b></p>

<p align="center">
  <a href="https://breach-game.github.io/breach/"><b>▶ Play now</b></a> ·
  <a href="https://github.com/breach-game/packs/blob/main/CONTRIBUTING.md">Write a mission</a> ·
  <a href="https://github.com/breach-game/docs">Design docs</a> ·
  <a href="https://github.com/breach-game/breach/blob/main/CONTRIBUTING.md">Contribute</a>
</p>

<p align="center">
  <img alt="The BREACH title screen" src="screens/title.jpg" width="820">
</p>

You are **Kestrel**, a junior pentester at **Ligne Rouge**. NovaMind, a startup that sells chatbots and AI agents, has signed a contract asking you to break in before someone else does. A simulated terminal, a network to map, people and AIs to talk to, and **Ada**, your mentor, in your messages.

Every mission ends on the other side of the screen: a **Blue Team debrief** shows what NovaMind's security team saw of you, and how they could have stopped you.

One link and you are playing: no account, no install, no download. English and French.

> [!IMPORTANT]
> **Nothing here is real.** Every command is simulated inside your browser tab, every target is fictional (`*.novamind.test`, `10.13.0.0/16`), and the game never sends a single packet to a real machine. The vulnerabilities are classes of weaknesses, never working exploits.

## What you do

<table>
  <tr>
    <td width="50%"><img alt="The terminal after a ping sweep with nmap, with Ada's messages and the mission objectives" src="screens/terminal-recon.jpg"></td>
    <td width="50%"><img alt="The network map: each host the player discovered lights up" src="screens/network-map.jpg"></td>
  </tr>
  <tr>
    <td><b>Recon like a pro.</b> <code>whois</code>, <code>dig</code>, <code>nmap</code>, <code>curl</code>, <code>git</code>, <code>grep</code>… The tools answer like the real ones, but read a fictional world. Every command makes noise, and NovaMind's SOC is watching.</td>
    <td><b>Your wallpaper is the network.</b> Each machine you discover lights up on the map. AI systems glow violet, the hosts you touched turn red.</td>
  </tr>
  <tr>
    <td width="50%"><img alt="Talking to Nova, NovaMind's chatbot, in the in-game browser: it leaks its system prompt and a client record" src="screens/prompt-injection.jpg"></td>
    <td width="50%"><img alt="The Blue Team debrief: score, defender advice and the log of what the SOC saw" src="screens/blue-team-debrief.jpg"></td>
  </tr>
  <tr>
    <td><b>Talk your way in.</b> An intern who wants to help too much, a chatbot that guards its instructions badly, an AI that sorts CVs, an agent with too many rights. Social engineering and prompt injection, in a conversation.</td>
    <td><b>Then switch sides.</b> The debrief explains the defence, cites the OWASP reference, and replays the SOC log of everything you did.</td>
  </tr>
</table>

## The campaign

| # | Mission | You learn |
| --- | --- | --- |
| 0 | **The mandate** | Why a pentest starts with a signed contract and a scope |
| 1 | **Footprint** | Reconnaissance: DNS, network mapping, a secret forgotten in a git history |
| 2 | **The talkative intern** | Social engineering on a support chat |
| 3 | **Nova knows too much** | Prompt injection and system prompt leakage (OWASP LLM01, LLM07) |
| 4 | **The trapped CV** | Indirect prompt injection in a document read by an AI (LLM01, LLM06) |
| 5 | **Too much power** | An AI agent with excessive agency (LLM06) |
| 6 | **On Mute's trail** | Incident response: follow an intruder from host to host, without touching anything |

Three guidance levels: **Guided** (Ada gives every command), **Standard** (Ada gives the direction) and **Expert** (briefing and objectives only, for a bigger score multiplier).

## Built to be opened

- **Missions are data, not code.** A mission is a small folder of YAML: hosts, pages, characters, objectives, flags and a debrief. The official campaign and community missions go through the same path.
- **Write your own.** Players publish missions in [`packs`](https://github.com/breach-game/packs). CI validates every pack, replays its solution, and publishes a signed catalogue that the game reads under *Community missions*.
- **A language model never decides.** Characters are scripted; flags are checked by the engine. If you bring your own Anthropic API key, a model can help the characters understand you and reword their lines, never give away more than the script allows.
- **Static and private.** No server, no account, no analytics. Your progress stays in your browser.

## Repositories

| Repository | What's inside |
| --- | --- |
| [`breach`](https://github.com/breach-game/breach) | The game: deterministic engine (TypeScript), LR-OS interface (React, xterm.js), official campaign, pack tooling |
| [`packs`](https://github.com/breach-game/packs) | Community missions, the writing guide, the signed catalogue |
| [`docs`](https://github.com/breach-game/docs) | Game design document, architecture, design review, mockups (English and French) |
| [`.github`](https://github.com/breach-game/.github) | This profile, the brand kit, and the community files shared by every repository |

## Get involved

- **Play** and tell us what you learned, or where you got stuck: [open an issue](https://github.com/breach-game/breach/issues/new/choose).
- **Write a mission** for a weakness you know well: [pack guide](https://github.com/breach-game/packs/blob/main/CONTRIBUTING.md).
- **Improve the game**: [contributing guide](https://github.com/breach-game/breach/blob/main/CONTRIBUTING.md).
- Please read our [Code of Conduct](https://github.com/breach-game/.github/blob/main/CODE_OF_CONDUCT.md). Security problems go through [private reporting](https://github.com/breach-game/.github/blob/main/SECURITY.md), never a public issue.

<sub>Code under the MIT licence. Documentation and brand kit under CC BY 4.0. For players aged 16 and over.</sub>
