# GuanZai · 观在

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

> 观而后动，众智自生。
> 深く観察し、ともに動き、絶えず進化する。

> **好钢用在刀刃上。贵模型也是一样。**
> *最良の鋼も、最良のモデルも、本当に必要な仕事のために取っておく。*

> **Codex × WorkBuddy：中西协作，各尽所长。**
> GuanZai は、Codex と WorkBuddy で利用可能なコスト効率の高いモデルを調和させ、能力・コスト・結果に応じて各タスクの経路を選択します。

**高度な知性は、本当に重要な場面にだけ使う。** GuanZai は、不必要な委任を避け、適した作業には低コストモデルを使い、高度な推論と独立レビューを最も重要な判断のために温存します。

東と西の出会い——万能薬ではないが、すべてのプレミアムトークンを価値あるものにする実用的な方法です。

> [!WARNING]
> **公開 Alpha — `v0.3.0-alpha.1`。** GuanZai が生成するのは計画とアダプターコマンドです。現時点では、完全な無人実行ループではありません。使用前にすべてのマニフェストとコマンドを確認してください。インターフェースとポリシーの詳細は変更される可能性があります。

## このリリースでできること

- タスクを決定論的に `solo`、`single`、`team`、または安全性によって優先される `audited` の計画に分類します。
- オーケストレーションの価値、アクションの影響、独立レビューを JSON マニフェストで明示します。
- 境界を定めたタスクパケットから、明示的な Codex CLI および WorkBuddy コマンドを構築します。
- `guanzai doctor` でローカルの Codex CLI と WorkBuddy CLI の機能を検出します。
- 大量の機械的作業を認知的な複雑さと取り違えないようにします。
- 現行ポリシーに合致する、意思決定に用いる金融作業と重大な変更には独立監査を要求します。
- インストール可能な Codex Skill と、ポリシー、ルーティング、パケット、CLI、機能を対象とする 42 件のテストを同梱します。

GuanZai は現在、生成したワーカーコマンドの起動、進捗のポーリング、結果の収集、または計画–実行–監査ループの自動完結を**行いません**。マニフェストの `"execution": "planned"` は、文字どおり計画済みであることだけを意味します。

## ポリシーの既定値

- WorkBuddy Hy3 / Hunyuan 3 (`hy3`) が最初の低コスト候補で、DeepSeek V4 Pro (`deepseek-v4-pro`) が次の WorkBuddy 階層です。
- WorkBuddy コマンドは常に `high` の推論強度を使用します。
- WorkBuddy GLM はブロックされます。
- Premium Fast/高速モードは禁止されています。生成される作業項目は標準速度を使用します。
- Codex のモデル選択は、ローカル Codex CLI が対応している場合にのみ利用できます。それ以外の Codex コラボレーションワーカーは、ホスト管理のモデル選択を引き継ぎます。
- 小さな予算によって独立チェックが暗黙に失われないよう、監査要件は要求されたワーカー予算を上書きできます。

これらは現在のコード上の既定値であり、モデル品質についての普遍的な主張ではありません。

## インストール

GuanZai には Python 3.9 以降が必要です。クローンしたリポジトリで次を実行します。

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

Windows では `python3` の代わりに `py` を使い、`.venv\Scripts\activate` で環境を有効化します。

Python パッケージがインストールするのは `guanzai` CLI だけです。同梱の Skill を Codex で利用できるようにするには、リポジトリのルートから別途インストールしてください。

```bash
mkdir -p ~/.codex/skills/guanzai
cp -R skill/guanzai/. ~/.codex/skills/guanzai/
```

Skill のインストールまたは更新後は Codex を再起動してください。Skill は Codex に GuanZai を呼び出すタイミングを案内しますが、計画されたアダプターコマンドを自動実行ループに変えるものではありません。

## クイックスタート

計画の対象とするプロジェクトで次を実行します。

```bash
guanzai init
guanzai doctor
guanzai plan "Research, design, implement, and verify a privacy-safe export" --json
```

`guanzai init` は `.guanzai/config.toml` と空のローカルメモリディレクトリを作成します。既存の設定は上書きしません。

範囲を限定したモードを指定するには、次を実行します。

```bash
guanzai plan "Rename these files using the existing pattern" --mode solo --json
guanzai plan "Implement the approved parser" --mode single --json
guanzai plan "Research, design, and verify the migration" --mode team --max-workers 3 --json
```

`audited` はコマンドラインで上書き指定するものではなく、ポリシーによって選択されます。アクションと影響が監査を必要とする場合、GuanZai は少なくとも実行者と監査者を一人ずつ維持します。

## モード

| モード | 意味 |
| --- | --- |
| `solo` | タスクをオーケストレーターに留め、ワーカー項目を作成しません。 |
| `single` | 境界を定めたワーカー項目を一つ作成します。 |
| `team` | 作業の広さや検証の必要性に見合う場合、相互補完する役割を作成します。 |
| `audited` | ポリシーに該当する重大な作業について独立監査者を維持し、安全でない予算を上書きします。 |

すべてのルーティングは決定論的で、現行のテキストポリシーに基づきます。説明可能でテストもできますが、意味を理解しているわけではありません。通常と異なる表現、他言語、または文脈の不足により、誤った計画が生成されることがあります。

## 機能の境界

`guanzai doctor` はローカルホストが公開できる機能を報告します。ルーターは常に計画を作成できますが、利用可能であることは実行済みであることを意味しません。

- ローカルに `codex` 実行ファイルがある場合、Codex CLI コマンド生成ではコマンドごとのモデルと推論設定を利用できます。
- 現在の Codex コラボレーションインターフェースは、サブエージェントごとのモデル選択を公開していません。これらのワーカーは引き続きホスト管理です。
- WorkBuddy の検出では、まず `PATH` 上の `codebuddy` を確認し、次に標準の macOS アプリケーションバンドルパスを確認します。
- WorkBuddy コマンドの生成は、WorkBuddy がインストール済み、認証済み、または指定モデルが利用可能であることを証明しません。

推奨や生成済みコマンドを、モデルが実行された証拠として扱わないでください。

## プライバシーとセキュリティ

GuanZai のリポジトリには認証情報ストアもクラウドサービスもありません。プロジェクト設定と将来のメモリは `.guanzai/` の下に置かれます。リポジトリの `.gitignore` は `.guanzai/` ディレクトリ全体を除外します。別の場所で GuanZai を使う場合もこのルールを維持し、ローカル状態を強制追加しないでください。生成されたタスクパケットには、入力したタスク本文が含まれることがあります。外部のエージェントやプロバイダーへ渡す前に確認してください。

機密性の高い作業で Alpha を使う前に、データ境界について[プライバシー](docs/PRIVACY.md)を、また[セキュリティ](SECURITY.md)をお読みください。脆弱性は公開 issue ではなく、GitHub の非公開脆弱性報告からお知らせください。

## アーキテクチャ

現在の経路は意図的に短くしています。

```text
task text -> deterministic value/risk gate -> role and model plan
          -> planned manifest -> optional adapter command construction
```

不変条件、コンポーネント、信頼境界については[アーキテクチャ](docs/ARCHITECTURE.md)をご覧ください。

## ロードマップ

- planned、started、completed、failed の状態を保持する永続的な実行台帳。
- オプトインの実行、ポーリング、キャンセル、正規化された結果、明示的な人間の承認点。
- 静的な選好だけでなく、観測された結果に基づく機能の調整。
- ACP/MCP 互換経路を含む、安定した契約による追加プロバイダーアダプター。
- バージョン管理されたルーティングポリシー、多言語ポリシー評価、安全なロールバック。
- 公開シード知識と非公開プロジェクトメモリの、より強い分離。

ロードマップ項目は意図であり、出荷済みの機能ではありません。

## 開発

```bash
python3 -m unittest discover -s tests -v
```

Windows での同等のコマンドは `py -m unittest discover -s tests -v` です。

現在のテストスイートには 42 件のテストがあります。[コントリビューション](CONTRIBUTING.md)、[行動規範](CODE_OF_CONDUCT.md)、[変更履歴](CHANGELOG.md)もご覧ください。

## 独立した開発と先行事例

GuanZai は独立したプロジェクトであり、Superpowers、CC Switch、MCO/Hive、LiteLLM、RouteLLM のフォークではありません。このリリースには、それらのプロジェクトからコピーしたソースコードはありません。それらのアイデアとエコシステムにおける取り組みは、ワークフロー、設定コントロールプレーン、複数 CLI の実行、ゲートウェイ、予算、ルーティング研究をめぐる境界を明確にする助けとなりました。

正確な謝辞については[先行事例](PRIOR_ART.md)と[第三者通知](THIRD_PARTY.md)をご覧ください。将来、第三者のソースをコピーまたは変更する場合は、そのライセンスと著作権表示も引き継ぐ必要があります。

## ライセンス

[MIT](LICENSE) © 2026 Dovesoup.
