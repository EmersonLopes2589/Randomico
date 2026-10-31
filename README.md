# Randomico

Aplicativo desktop em Python para simular o sorteio da Mega-Sena com animação visual, números revelados um a um e efeitos sonoros.

## Visão geral

O projeto cria uma interface gráfica em Tkinter com um desenho estilizado de sorteio de loteria:

- 6 bolas com números aleatórios de 1 a 60
- animação de embaralhamento
- revelação dos números em sequência
- confete ao final do sorteio
- som de toque e fanfarra de vitória
- botão para ativar/desativar os sons

## Funcionalidades

- Sorteio de 6 números únicos
- Ordenação dos números sorteados
- Visualização em tela com estética inspirada na Mega-Sena
- Animação de bolas quicando e revelando números
- Efeito de confete após o sorteio
- Alternância do áudio com um botão

## Requisitos

- Python 3.8 ou superior
- Sistema operacional Windows
- Tkinter (normalmente incluído na instalação do Python no Windows)

## Como executar

1. Clone o repositório:

```bash
git clone https://github.com/EmersonLopes2589/Randomico.git
cd Randomico
```

2. Execute o script:

```bash
python Randomico.py
```

Se o comando `python` não estiver disponível, tente:

```bash
python3 Randomico.py
```

## Estrutura do projeto

```text
Randomico/
├── Randomico.py
└── README.md
```

## Observações

- O projeto utiliza a biblioteca `winsound`, que é específica do Windows, então ele não funciona nativamente em Linux ou macOS.
- A interface gráfica foi construída com `tkinter`, que é uma biblioteca padrão do Python.

## Licença

Este projeto não possui licença definida no repositório.

## Autor

Emerson Lopes

## Observação

Se quiser, posso também criar uma versão mais refinada do README com badges, screenshots e instruções para instalação em ambientes Windows e Python virtual.
