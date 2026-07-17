# GuanZai · 观在

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

> 观而后动，众智自生。
> 깊이 살피고, 함께 행동하며, 계속 진화합니다.

> **好钢用在刀刃上。贵模型也是一样。**
> *가장 좋은 강철도, 가장 비싼 모델도, 진정으로 필요한 작업을 위해 남겨두세요.*

> **Codex × WorkBuddy：中西协作，各尽所长。**
> GuanZai는 Codex를 WorkBuddy에서 사용할 수 있는 비용 효율적인 모델과 조화시켜, 능력·비용·결과에 따라 각 작업의 경로를 선택합니다.

**고급 지능은 정말 중요한 순간에만 사용하세요.** GuanZai는 불필요한 위임을 피하고, 적합한 작업에는 저비용 모델을 사용하며, 고급 추론과 독립 검토를 가장 중요한 결정을 위해 보존합니다.

동양과 서양의 만남——만병통치약은 아니지만, 모든 프리미엄 토큰을 가치 있게 만드는 실용적인 방법입니다.

> [!WARNING]
> **공개 Alpha — `v0.3.0-alpha.1`.** GuanZai는 계획과 어댑터 명령을 생성합니다. 아직 완전한 무인 실행 루프가 아닙니다. 사용하기 전에 모든 매니페스트와 명령을 검토하세요. 인터페이스와 정책 세부 사항은 변경될 수 있습니다.

## 이번 릴리스에서 제공하는 기능

- 작업을 결정론적으로 `solo`, `single`, `team` 또는 안전 정책이 우선하는 `audited` 계획으로 분류합니다.
- 오케스트레이션의 가치, 작업의 영향, 독립 검토를 JSON 매니페스트에 명시합니다.
- 범위가 제한된 작업 패킷에서 명시적인 Codex CLI 및 WorkBuddy 명령을 구성합니다.
- `guanzai doctor`로 로컬 Codex CLI와 WorkBuddy CLI 기능을 감지합니다.
- 대량의 기계적 작업을 인지적 복잡성으로 오인하지 않도록 합니다.
- 현행 정책에 해당하는 의사결정용 금융 작업과 중대한 변경에 독립 감사를 요구합니다.
- 설치 가능한 Codex Skill과 정책, 라우팅, 패킷, CLI, 기능을 다루는 42개 테스트를 제공합니다.

현재 GuanZai는 생성된 워커 명령을 실행하거나, 진행 상황을 폴링하거나, 결과를 수집하거나, 계획–실행–감사 루프를 자동으로 닫지 **않습니다**. 매니페스트의 `"execution": "planned"`는 말 그대로 계획되었다는 뜻입니다.

## 기본 정책

- WorkBuddy Hy3 / Hunyuan 3 (`hy3`)이 첫 번째 저비용 선택이며, DeepSeek V4 Pro (`deepseek-v4-pro`)가 그다음 WorkBuddy 등급입니다.
- WorkBuddy 명령은 항상 `high` 추론 강도를 사용합니다.
- WorkBuddy GLM은 차단됩니다.
- Premium Fast/고속 모드는 금지됩니다. 생성된 작업 항목은 표준 속도를 사용합니다.
- Codex 모델 선택은 로컬 Codex CLI가 지원하는 경우에만 사용할 수 있습니다. 그 외의 Codex 협업 워커는 호스트가 관리하는 모델 선택을 따릅니다.
- 작은 예산이 독립 검사를 암묵적으로 없애서는 안 되므로, 감사 요구 사항은 요청된 워커 예산보다 우선할 수 있습니다.

이는 현재 코드의 기본값이며, 모델 품질에 대한 보편적인 주장이 아닙니다.

## 설치

GuanZai에는 Python 3.9 이상이 필요합니다. 복제한 저장소에서 다음을 실행하세요.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

Windows에서는 `python3` 대신 `py`를 사용하고 `.venv\Scripts\activate`로 환경을 활성화하세요.

Python 패키지는 `guanzai` CLI만 설치합니다. 번들 Skill을 Codex에서 사용할 수 있게 하려면 저장소 루트에서 별도로 설치하세요.

```bash
mkdir -p ~/.codex/skills/guanzai
cp -R skill/guanzai/. ~/.codex/skills/guanzai/
```

Skill을 설치하거나 업데이트한 뒤 Codex를 다시 시작하세요. Skill은 Codex가 언제 GuanZai를 호출할지 안내하지만, 계획된 어댑터 명령을 자동 실행 루프로 바꾸지는 않습니다.

## 빠른 시작

계획하려는 프로젝트에서 다음을 실행하세요.

```bash
guanzai init
guanzai doctor
guanzai plan "Research, design, implement, and verify a privacy-safe export" --json
```

`guanzai init`은 `.guanzai/config.toml`과 빈 로컬 메모리 디렉터리를 만듭니다. 기존 설정은 덮어쓰지 않습니다.

범위가 제한된 모드를 요청하려면 다음을 실행하세요.

```bash
guanzai plan "Rename these files using the existing pattern" --mode solo --json
guanzai plan "Implement the approved parser" --mode single --json
guanzai plan "Research, design, and verify the migration" --mode team --max-workers 3 --json
```

`audited`는 명령줄 재정의 옵션이 아니라 정책에 의해 선택됩니다. 작업과 영향에 감사가 필요하면 GuanZai는 최소한 실행자 한 명과 감사자 한 명을 유지합니다.

## 모드

| 모드 | 의미 |
| --- | --- |
| `solo` | 작업을 오케스트레이터가 유지하며 워커 항목을 만들지 않습니다. |
| `single` | 범위가 제한된 워커 항목 하나를 만듭니다. |
| `team` | 작업 범위나 검증 필요성이 충분한 경우 상호 보완적인 역할을 만듭니다. |
| `audited` | 정책에 해당하는 중대한 작업에 독립 감사자를 유지하며 안전하지 않은 예산보다 우선합니다. |

모든 라우팅은 결정론적이며 현재의 텍스트 정책에 기반합니다. 설명하고 테스트할 수 있지만 의미론적 이해는 아닙니다. 평소와 다른 표현, 다른 언어 또는 부족한 맥락으로 인해 잘못된 계획이 생성될 수 있습니다.

## 기능 경계

`guanzai doctor`는 로컬 호스트가 제공할 수 있는 기능을 보고합니다. 라우터는 언제든 계획을 만들 수 있지만, 사용 가능하다는 것이 실행되었다는 뜻은 아닙니다.

- 로컬에 `codex` 실행 파일이 있으면 Codex CLI 명령 생성에서 명령별 모델 및 추론 설정을 지원합니다.
- 현재 Codex 협업 인터페이스는 하위 에이전트별 모델 선택을 제공하지 않습니다. 해당 워커의 모델은 계속 호스트가 관리합니다.
- WorkBuddy 탐색은 먼저 `PATH`의 `codebuddy`를 확인한 다음 표준 macOS 애플리케이션 번들 경로를 확인합니다.
- WorkBuddy 명령 생성은 WorkBuddy가 설치 또는 인증되었거나 지정한 모델을 사용할 수 있다는 증거가 아닙니다.

추천이나 생성된 명령을 모델이 실행되었다는 증거로 간주하지 마세요.

## 개인정보 보호 및 보안

GuanZai 저장소에는 자격 증명 저장소나 클라우드 서비스가 없습니다. 프로젝트 설정과 향후 메모리는 `.guanzai/` 아래에 있습니다. 저장소의 `.gitignore`는 `.guanzai/` 디렉터리 전체를 제외합니다. 다른 곳에서 GuanZai를 사용할 때도 이 규칙을 유지하고 로컬 상태를 강제로 추가하지 마세요. 생성된 작업 패킷에는 사용자가 제공한 작업 텍스트가 포함될 수 있습니다. 외부 에이전트나 제공업체에 전달하기 전에 검토하세요.

민감한 작업에 Alpha를 사용하기 전에 데이터 경계를 설명하는 [개인정보 보호](docs/PRIVACY.md)와 [보안](SECURITY.md) 문서를 읽어보세요. 취약점은 공개 issue가 아닌 GitHub 비공개 취약점 보고 기능으로 알려주세요.

## 아키텍처

현재 경로는 의도적으로 짧게 유지됩니다.

```text
task text -> deterministic value/risk gate -> role and model plan
          -> planned manifest -> optional adapter command construction
```

불변 조건, 구성 요소, 신뢰 경계는 [아키텍처](docs/ARCHITECTURE.md)를 참고하세요.

## 로드맵

- planned, started, completed, failed 상태를 보존하는 지속형 실행 원장.
- 사용자가 선택하는 실행, 폴링, 취소, 정규화된 결과 및 명시적인 사람의 승인 지점.
- 정적인 선호만이 아니라 관찰된 결과를 바탕으로 한 기능 보정.
- ACP/MCP 호환 경로를 포함해 안정적인 계약을 통한 추가 제공업체 어댑터.
- 버전이 지정된 라우팅 정책, 다국어 정책 평가 및 안전한 롤백.
- 공개 시드 지식과 비공개 프로젝트 메모리의 더 강한 분리.

로드맵 항목은 의도일 뿐, 출시된 기능이 아닙니다.

## 개발

```bash
python3 -m unittest discover -s tests -v
```

Windows에서 동일한 명령은 `py -m unittest discover -s tests -v`입니다.

현재 테스트 모음에는 42개 테스트가 있습니다. [기여 안내](CONTRIBUTING.md), [행동 강령](CODE_OF_CONDUCT.md), [변경 기록](CHANGELOG.md)을 참고하세요.

## 독립 작업과 선행 사례

GuanZai는 독립 프로젝트이며 Superpowers, CC Switch, MCO/Hive, LiteLLM 또는 RouteLLM의 포크가 아닙니다. 이번 릴리스에는 해당 프로젝트의 소스 코드를 복사하지 않았습니다. 그 프로젝트들의 아이디어와 생태계 작업은 워크플로, 구성 제어 영역, 다중 CLI 실행, 게이트웨이, 예산 및 라우팅 연구의 경계를 분명히 하는 데 도움이 되었습니다.

정확한 감사 표시는 [선행 사례](PRIOR_ART.md)와 [서드파티 고지](THIRD_PARTY.md)를 참고하세요. 향후 서드파티 소스를 복사하거나 수정한다면 해당 라이선스와 저작권 고지도 함께 포함해야 합니다.

## 라이선스

[MIT](LICENSE) © 2026 Dovesoup.
