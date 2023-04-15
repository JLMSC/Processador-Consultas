# **Processador-Consultas**
Implementação de um **Processador de Consultas** em **Python 3**.

### **Funcionalidades principais**
1. Parser (Análise) de uma consulta SQL;
2. Geração do grafo de operadores da consulta;
3. Ordem de execução da consulta;
4. Exibição dos resultados na interface gráfica

##### O Parser está **LIMITADO** para *"Select", "From", "Where", "Join On"* e, também, para os operadores *"=", ">", "<", "<=", ">=", "<>", "And", "In", "Not In", "(", ")"*.

## **As maravilhosas Expresões Regulares utilizadas.**
`\b(select|from|join|on|where)\b|(;$)`
* `\b` - Delimitador, indica que alguma coisa deve começar, ou terminar *(depende de sua posição no RegEx)*, com um caractere específico.
* `(select|from|join|on|where)` - Captura em um grupo as seguintes palavras: *"select, from, join, on"* ou *"where"*.
* `|` - Operador *OR*.
* `(;&)` - Captura em um grupo o *";"*, porém este deve estar localizado ao final de um texto.
> Essa expressão regular tem como objetivo separar algumas *palavras reservadas* do comando SQL.

`\*|^[a-zA-Z]+[a-zA-Z0-9_]*(,\s*[a-zA-Z]+[a-zA-Z0-9_]*)*$|^[a-zA-Z]+[a-zA-Z0-9_]*\.[a-zA-Z]+[a-zA-Z0-9_]*(,\s*[a-zA-Z]+[a-zA-Z0-9_]*\.[a-zA-Z]+[a-zA-Z0-9_]*)*$`
###### *~~Eu não sei como eu cheguei nesse resultado mas só de olhar da dor de cabeça~~*
* `\*` - Captura o *"\*"*, é isso.
* `|` - Operador *OR*.
* `^[a-zA-Z]+[a-zA-Z0-9_]*(,\s*[a-zA-Z]+[a-zA-Z0-9_]*)*$` - Captura parâmetros únicos ou separados por uma vírgula, em que esses parâmetros devem começar com uma letra, sendo minúsucula ou maiúsucla e pode ter qualquer quantia de letras, dígitos e *_ (underline)*.
* `^[a-zA-Z]+[a-zA-Z0-9_]*\.[a-zA-Z]+[a-zA-Z0-9_]*(,\s*[a-zA-Z]+[a-zA-Z0-9_]*\.[a-zA-Z]+[a-zA-Z0-9_]*)*$` - Captura parâmetros únicos ou separados por uma vírgula, no formato "nomeTabela.nomeColuna", em que esses parâmetros devem começar com uma letra, sendo minúscula ou maiúscula e pode ter qualquer quantia de letras, dígitos e *_ (underline)*, ai tem o *.* e o mesmo é aplicado pro texto além do ponto.
> Entradas como `123foo.bar`, `usuario.nome, usuario.idade` e dentre outros **NÃO** serão aceitos.