# verificador_python
Início do projeto piloto de verificador de sistemas em Python

Este projeto piloto propõe o desenvolvimento e documentação de um sistema modular e extensível de verificação de software em Python, voltado para aplicações com requisitos críticos como confiabilidade, segurança e comportamento determinístico. A proposta central é unir, em uma única plataforma, técnicas tradicionais de análise estática, verificação formal simbólica e testes automatizados baseados em propriedades, de modo a fornecer uma visão ampla e estruturada da confiabilidade de sistemas implementados em Python.


Para uso do projeto:

mkdir python_verificador

cd python_verificador

git clone https://github.com/charlesuchoa/verificador_python.git


Para do sistema é necessário a instalação de:

Python 3.8.10 ou superior

e uso do arquivo requirements.txt para instalação das bibliotecas:

bandit

flake8

z3-solver

hypothesis

pytest

rich

reportlab


Uso da aplicação:

por linha de comando: 

python main.py nome_do_arquivo.py --run-z3 (com uso do Z3)

python main.py nome_do_arquivo.py (com uso do Flake e Bandit)


podem ser utilizados também os seguintes parâmetros após o nome_do_arquivo.py:

--run-z3  		-> Executa a verificação formal com SMT solver. 

--solver \[z3      | cvc5        | boolector]\   -> Define o solver SMT a ser utilizado. Padrão: `z3`. 

--z3-incremental	-> Ativa o modo incremental de verificação com o solver Z3.

--run-hypothesis	-> Executa testes automatizados com a biblioteca Hypothesis.

--context-switch N` 	-> Nível de comutação de contexto simulado (reserva para multithreading).

--skip-static		-> Ignora os analisadores estáticos Bandit e Flake8.
