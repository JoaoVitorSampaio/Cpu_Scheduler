# 🧠 Escalonador de Processos — Python

## 📄 Descrição

Este projeto implementa um **escalonador de CPU** em Python, simulando três algoritmos clássicos de escalonamento de processos:

- 🕐 **FCFS**: First-Come, First-Served
- ⚡ **SJF**: Shortest Job First (não-preemptivo)
- 🔄 **RR**: Round Robin (com quantum fixo = 2)

O programa **lê os processos a partir de um arquivo `input.txt`**, contendo pares `tempo_chegada tempo_duração`, e exibe as **médias de tempo de retorno, resposta e espera**, formatadas com uma casa decimal e separador decimal `,` (vírgula).

---

## 📁 Estrutura do Projeto

```
.
├── input.txt            # Arquivo de entrada com os processos
├── main.py              # Código-fonte principal do escalonador
├── README.md            # Este arquivo
```

---

## ▶️ Como Executar

### 1. 💾 Adicione os dados de entrada no arquivo `input.txt`

Cada linha deve conter **dois inteiros** separados por espaço:

```
<tempo_de_chegada> <tempo_de_duracao>
```

Exemplo:

```
0 10
4 4
8 6
21 8
```

### 2. ▶️ Execute o programa com Python 3

```bash
python3 main.py
```

---

## 📤 Exemplo de Saída

```
FCFS: 10,0 3,0 3,0
SJF: 10,0 3,0 3,0
RR: 11,0 0,5 4,0
```

Cada linha corresponde a um algoritmo, seguido das **médias** em ordem:

1. ⏱ Tempo de **retorno**
2. 🎯 Tempo de **resposta**
3. 🕓 Tempo de **espera**

---

## ⚙️ Algoritmos Implementados

- ✅ FCFS (ordena os processos pela chegada e executa sequencialmente)
- ✅ SJF não-preemptivo (seleciona o processo com menor duração entre os disponíveis)
- ✅ RR com quantum 2 (executa por fatias de tempo circulares)

Todos os algoritmos computam as métricas conforme as definições:

- **Tempo de retorno** = tempo de término − tempo de chegada
- **Tempo de espera** = tempo de retorno − duração
- **Tempo de resposta** = primeiro tempo de execução − chegada

---

## ⚠️ Observações

- O arquivo `input.txt` deve estar no **mesmo diretório** do `main.py`.
- Linhas inválidas na entrada serão **ignoradas automaticamente**.
- O programa segue rigorosamente o **formato exigido** para avaliação automática.
- Não são utilizados módulos externos — 100% Python puro.
