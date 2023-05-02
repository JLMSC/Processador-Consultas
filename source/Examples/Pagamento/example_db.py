"""Arquivo responsável pela representação de
um banco de dados exemplar."""

from typing import Dict, List

pagamento_example_db: Dict[str, List[str]] = {
    "usuario": [
        "idusuario", "nome", "logradouro", "número",
        "bairro", "cep", "uf", "datanascimento"
    ],
    "contas": [
        "idconta", "descricao", "tipoconta_idtipoconta",
        "usuario_idusuario", "saldoinicial"
    ],
    "movimentacao": [
        "idmovimentacao", "datamovimentacao", "descricao",
        "tipomovimento_idtipomovimento", "categoria_idcategoria",
        "contas_idconta", "valor"
    ],
    "tipomovimentacao": [
        "idtipomovimentacao", "descmovimentacao"
    ],
    "categoria": [
        "idcategoria", "desccategoria"
    ],
    "tipoconta": [
        "idtipoconta", "descrição"
    ]
}