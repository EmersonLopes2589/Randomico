# Randomico

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=microsoft&logoColor=white" alt="Windows" />
  <img src="https://img.shields.io/badge/GUI-Tkinter-00A6A6?style=for-the-badge" alt="Tkinter" />
</div>

Aplicativo desktop em Python que simula o sorteio da Mega-Sena com animação visual, efeito de confete, revelação dos números e sons de loteria.

## Descrição

O Randomico é um projeto simples e visualmente dinâmico para gerar sorteios de loteria em uma interface gráfica. A aplicação exibe seis bolas, embaralha números aleatórios de 1 a 60, revela cada uma em sequência e finaliza com uma animação celebrativa.

A interface foi construída com `tkinter`, e os efeitos sonoros usam `winsound`, que é nativo do Windows.

## Funcionalidades

- Sorteio de 6 números únicos de 1 a 60
- Ordenação automática dos números sorteados
- Animação de embaralhamento com efeito de quique
- Revelação dos números um por um
- Confete animado ao final do sorteio
- Efeito sonoro durante o processo e na vitória
- Botão para ativar/desativar os sons
- Interface gráfica com visual inspirado em sorteios de loteria

## Demonstração

A aplicação apresenta uma janela com:

- título do sorteio
- seis bolas estilizadas
- botão para sortear novamente
- indicador de status do sorteio
- opção para ligar/desligar o som

## Requisitos

Antes de executar o projeto, verifique se você possui:

- Python 3.8 ou superior
- Sistema operacional Windows
- Biblioteca padrão `tkinter`
- Acesso ao módulo `winsound` (disponível no Windows)

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/EmersonLopes2589/Randomico.git
cd Randomico
```

2. Verifique se o Python está instalado:

```bash
python --version
```

3. Execute o script principal:

```bash
python Randomico.py
```

Se o comando `python` não estiver disponível no ambiente, tente:

```bash
python3 Randomico.py
```

## Estrutura do projeto

```text
Randomico/
├── Randomico.py
├── README.md
└── .gitignore
```

## Como funciona

O processo da aplicação segue esta lógica:

1. Gera 6 números aleatórios distintos entre 1 e 60
2. Embaralha e exibe a animação de sorteio
3. Revela cada número em sequência
4. Finaliza a tela com a combinação sorteada
5. Aciona o confete e a fanfarra de vitória

## Observações importantes

- O projeto foi desenvolvido para Windows, pois usa `winsound`.
- Em Linux ou macOS, o código pode falhar ou não reproduzir áudio corretamente.
- A interface é construída com `tkinter`, que normalmente já vem instalado com o Python no Windows.

## Tecnologias utilizadas

- Python
- Tkinter
- Random
- Threading
- winsound

## Licença

Este repositório não possui uma licença definida no momento.

## Autor

Emerson Lopes

## Contato

Se você quiser contribuir, sugerir melhorias ou testar o projeto, fique à vontade para abrir uma issue ou enviar um pull request.
