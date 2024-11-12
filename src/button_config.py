def get_button_data():
    return {
        "PRINCIPAL": [
            ("Abertura e\nFechamento\nde Caixa", "icon/caixa.ico", "handle_caixa", "button-caixa"),
            ("Adicionar Pedido", "icon/pedido.ico", "open_adicionar_pedido", "button-adicionar-pedido"),
            ("Histórico de\nFechamentos", "icon/historico.ico", "open_historico", "button-historico"),
            ("Relatórios", "icon/relatorios.ico", "open_tab", "button-relatorios", "Relatórios"),
            ("Alertas", "icon/alert_icon.ico", "open_tab", "button-alertas", "Alertas"),
            ("Controle de\nOrçamento", "icon/orçamento.ico", "open_tab", "button-orcamento", "Controle de Orçamento"),
            ("Importação e\nExportação", "icon/import.ico", "open_tab", "button-import", "Importação/Exportação"),
            ("Relatórios de\nFechamento", "icon/relatorio.ico", "open_tab", "button-relatorio-fechamento", "Relatórios de Fechamento"),
            ("Sair", "icon/sair.ico", "close_app", "button-sair")
        ],
        "PRODUTOS": [
            ("Produtos", "icon/produtos.ico", "produtos_callback", "produtos_button"),
            ("Complementos", "icon/complementos.ico", "complementos_callback", "complementos_button"),
            ("Observações", "icon/observacoes.ico", "observacoes_callback", "observacoes_button"),
            ("Categorias", "icon/categorias.ico", "categorias_callback", "categorias_button"),
            ("Tipos e Tamanhos", "icon/tipos.ico", "tipos_tamanhos_callback", "tipos_tamanhos_button"),
            ("Perguntas", "icon/perguntas.ico", "perguntas_callback", "perguntas_button"),
            ("Insumos", "icon/insumos.ico", "insumos_callback", "insumos_button"),
            ("Alterar Estoque\nem Lote", "icon/alterar_estoque.ico", "alterar_estoque_lote_callback", "alterar_estoque_lote_button"),
            ("Alterar Estoque\ncom NFe", "icon/alterar_estoque_nfe.ico", "alterar_estoque_nfe_callback", "alterar_estoque_nfe_button"),
            ("Histórico de\nEntradas e Saídas", "icon/historico_entradas.ico", "historico_entradas_saidas_callback", "historico_entradas_saidas_button"),
            ("Posição por Data", "icon/posicao.ico", "posicao_data_callback", "posicao_data_button"),
            ("Promoções", "icon/promocoes.ico", "promocoes_callback", "promocoes_button"),
            ("Histórico de\nItens Vendidos", "icon/historico_itens.ico", "historico_itens_vendidos_callback", "historico_itens_vendidos_button")
        ],
        "FINANCEIRO": [
            ("9", "icon/busca.ico", "open_tab", "button-financeiro-9", "9"),
            ("10", "icon/busca.ico", "open_tab", "button-financeiro-10", "10"),
            ("11", "icon/busca.ico", "open_tab", "button-financeiro-11", "11"),
            ("12", "icon/busca.ico", "open_tab", "button-financeiro-12", "12"),
            ("13", "icon/busca.ico", "open_tab", "button-financeiro-13", "13"),
            ("14", "icon/busca.ico", "open_tab", "button-financeiro-14", "14"),
            ("15", "icon/busca.ico", "open_tab", "button-financeiro-15", "15"),
            ("16", "icon/busca.ico", "open_tab", "button-financeiro-16", "16")
        ],
        "CONFIGURAÇÕES": [
            ("modo dark", "icon/dark.ico", "toggle_dark_mode", "button-config-dark"),
            ("18", "icon/busca.ico", "open_tab", "button-config-18", "18"),
            ("19", "icon/busca.ico", "open_tab", "button-config-19", "19"),
            ("20", "icon/busca.ico", "open_tab", "button-config-20", "20"),
            ("21", "icon/busca.ico", "open_tab", "button-config-21", "21"),
            ("22", "icon/busca.ico", "open_tab", "button-config-22", "22"),
            ("23", "icon/busca.ico", "open_tab", "button-config-23", "23"),
            ("24", "icon/busca.ico", "open_tab", "button-config-24", "24")
        ],
        "APPS": [
            ("25", "icon/busca.ico", "open_tab", "button-app-25", "25"),
            ("26", "icon/busca.ico", "open_tab", "button-app-26", "26"),
            ("27", "icon/busca.ico", "open_tab", "button-app-27", "27"),
            ("28", "icon/busca.ico", "open_tab", "button-app-28", "28"),
            ("29", "icon/busca.ico", "open_tab", "button-app-29", "29"),
            ("30", "icon/busca.ico", "open_tab", "button-app-30", "30"),
            ("31", "icon/busca.ico", "open_tab", "button-app-31", "31"),
            ("32", "icon/busca.ico", "open_tab", "button-app-32", "32")
        ],
    }