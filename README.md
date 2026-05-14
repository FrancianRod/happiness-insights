# 🌍 Happiness Insights — World Happiness Report Analysis

Análise exploratória dos dados do **World Happiness Report** (2016 e 2019), com limpeza de dados, visualizações interativas em Plotly e narrativa analítica. Projeto desenvolvido como parte de um estudo em análise de dados com foco em bem-estar global.

---

## 📁 Estrutura do Projeto

```
happiness-insights/
│
├── data/
│   ├── 2016.csv          # Dataset WHR 2016
│   └── 2019.csv          # Dataset WHR 2019
│
├── src/
│   ├── analysis_2016.py  # Script completo para o ano 2016
│   └── analysis_2019.py  # Script completo para o ano 2019
│
├── outputs/              # Gráficos e artefatos gerados localmente
│   └── .gitkeep
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📊 O que o projeto faz

Cada script de análise executa as seguintes etapas:

### 1. Verificação e limpeza de dados
- Checagem dos tipos de dados de cada coluna
- Remoção de espaços em branco em colunas de texto
- Substituição de strings vazias por `NaN`
- Conversão para os tipos corretos (`float64`, `Int64`, `StringDtype`)
- Identificação e preenchimento de valores ausentes com a média da coluna

### 2. Visualizações com Plotly

| Figura | Tipo | Descrição |
|--------|------|-----------|
| `fig1` | Gráfico de barras agrupado | GDP per Capita e Expectativa de Vida dos Top 10 países |
| `fig2` | Heatmap de correlação | Relação entre os 7 fatores de felicidade |
| `fig3` | Gráfico de dispersão | Efeito do GDP per Capita no Score de Felicidade por grupo |
| `fig4` | Gráfico de pizza | Score médio de Felicidade por Região / Faixa de GDP |
| `fig5` | Mapa coroplético | GDP per Capita por país com tooltip de Expectativa de Vida |

### 3. Narrativa analítica
Cada script imprime no terminal uma narrativa completa com os principais insights de cada visualização e conclusões gerais.

---

## ⚙️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/happiness-insights.git
cd happiness-insights
```

### 2. Crie um ambiente virtual e instale as dependências

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Execute os scripts

```bash
# Análise do ano 2016
python src/analysis_2016.py

# Análise do ano 2019
python src/analysis_2019.py
```

Os gráficos abrirão automaticamente no navegador via Plotly.

---

## 📦 Dependências

| Biblioteca | Versão mínima |
|------------|---------------|
| pandas     | 2.0.0         |
| numpy      | 1.24.0        |
| plotly     | 5.18.0        |

---

## 🗃️ Sobre os dados

Os dados são do **World Happiness Report**, disponíveis publicamente no [Kaggle](https://www.kaggle.com/datasets/unsdsn/world-happiness) sob licença **CC0: Public Domain**.

### Colunas — 2016

| Coluna | Descrição |
|--------|-----------|
| Country | Nome do país |
| Region | Região geográfica |
| Happiness Rank | Classificação por felicidade |
| Happiness Score | Pontuação de felicidade |
| Economy (GDP per Capita) | Contribuição do PIB |
| Family | Contribuição da família |
| Health (Life Expectancy) | Contribuição da saúde |
| Freedom | Contribuição da liberdade |
| Trust (Government Corruption) | Contribuição da confiança |
| Generosity | Contribuição da generosidade |
| Dystopia Residual | Resíduo de distopia |

### Colunas — 2019

| Coluna | Descrição |
|--------|-----------|
| Overall rank | Classificação geral |
| Country or region | Nome do país ou região |
| Score | Pontuação de felicidade |
| GDP per capita | PIB per capita |
| Social support | Suporte social |
| Healthy life expectancy | Expectativa de vida saudável |
| Freedom to make life choices | Liberdade de escolha |
| Generosity | Generosidade |
| Perceptions of corruption | Percepção de corrupção |

> ⚠️ O dataset de 2019 não possui coluna `Region`. O script cria automaticamente uma coluna `GDP Tier` (Low / Lower-Middle / Upper-Middle / High) como proxy para agrupamento.

---

## 💡 Principais insights

- **GDP per Capita** e **Expectativa de Vida** são os maiores preditores de felicidade em ambos os anos
- **Europa Ocidental** e **América do Norte** concentram os maiores scores de felicidade
- **África Subsaariana** apresenta os menores scores, reflexo de desigualdade estrutural
- A **América Latina** apresenta um "prêmio de felicidade" — scores acima do esperado pelo GDP, explicado por laços sociais fortes
- **Liberdade** e **Suporte Social** têm impacto relevante além do fator econômico

---

## 👩‍💻 Autora

Desenvolvido por **Francian** como projeto de análise de dados com foco em bem-estar global.

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).  
Os dados utilizados estão sob licença **CC0: Public Domain**.
