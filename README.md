*This project has been created as part of the 42 curriculum by gabrieol, joao-ped.*

# Descrição

"A-Maze-ing" é um programa em python que constroi, gerencia e exibe um labirinto (em uma janela separada ou no terminal). O desafio aqui é criar um módulo standalone com o algoritmo de criação do labirinto, o de resolução do labirinto e um método de criação do arquivo que representa o labirinto criado, com cada cela em hexadecimal, coordenadas de saída e de entrada e o caminho para a saída.

# Instruções

Antes de qualquer coisa, é recomendado criar uma venv para rodar o programa com ela usando "make install" e rodar "pip install -r requirements.txt" para instalar o mypy e o flake8 para checar a norma com "make lint" e/ou "make lint-strict".
Após tudo isso, rodando "make run" no terminal, o labirinto é exibido junto com um menu com 4 opções:

1. Gera um novo labirinto (que se a seed for inserida no config.txt vai ser idêntico)
2. Exibe e oculta o caminho para a saída no labirinto
3. Troca a cor do labirinto
4. Fecha o programa.

# Recursos

- https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/ (Demonstração do algoritmo usado para a criação do labirinto)
- https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/ (Demonstração do algoritmo usado para a solução do labirinto)
- https://github.com/LunnaBoo/A_Maze_ing_Guide/wiki (Um guia geral criado por luccribe e thasampa)

# config.txt

É necessário um arquivo "config.txt" com as seguintes informações do labirinto (a ordem não importa):

- WIDTH: Um número representando a largura do labirinto
- HEIGHT: Um número representando a altura do labirinto
- ENTRY: As coordenadas da entrada do labirinto no formato x,y
- EXIT: As coordenadas da saída do labirinto no formato x,y
- OUTPUT_FILE: O nome do arquivo a ser gerado com as informações do labirinto
- PERFECT: True ou False, True gerando um labirinto com apenas um caminho entre a entrada e a saída, e False com diversos caminhos
- SEED: Um número que fará o mesmo labirinto ser gerado sempre. Este parâmetro é opicional

Cada informação deve ser escrita em uma linha separada no formato "KEY=VALUE".

# Algoritmos

Para a geração do labirinto em si, primeiro é gerado um "labirinto" com todas as paredes fechadas, e com o algoritmo DFS, as paredes são quebradas. Para a resolução do labirinto, o BFS é usado, "andando" até achar uma parede (e então começa a retornar a última cela com algum caminho) ou a saída.
Os algoritmos são quase como irmãos, funcionando de maneiras muito parecidas. A escolha dos dois veio dessa semelhança e também da simplicidade de ambos, pois funcionam para qualquer coisa com uma estrutura semelhante ao programa.

# Reusabilidade

Na classe MazeGenerator, cada funcionalidade do labirinto está separado em um método próprio, fornecendo um controle total sobre o labirinto, mas de um jeito simples também. A classe Pallet e suas derivadas também são fornecidas, a primeira para criar uma palheta e as derivadas são cores já fornecidas para o labirintos. As classes Cell e Config também podem ser usadas, porém servem mais para auxílio da classe MazeGenerator, não para uso individual. O menu está no main.py, não é fornecido no módulo.

# Equipe

Também contando com a ajuda de Gaya (gmarinho), Brits (jbrits-m) Nahirim (naportel) e Gustavo (gustada-), nós dois (gabrieol e joao-ped) fizemos tudo do início ao fim, sem realmente separar funções.
