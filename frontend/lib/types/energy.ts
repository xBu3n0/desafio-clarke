export type DataSource = "rest" | "graphql";

export type Estado = {
  id: number;
  nome: string;
  sigla: string;
  tarifaBaseKwh: string;
};

export type FornecedorComparacao = {
  id: number;
  nome: string;
  numeroClientes: number;
  avaliacaoMedia: number;
  logoUrl: string;
  custoKwh: number;
  custoFornecedor: number;
  economia: number;
  economiaPercentual: number;
};

export type SolucaoComparacao = {
  solucao: "GD" | "Mercado Livre";
  fornecedores: FornecedorComparacao[];
};

export type FormErrors = {
  estadoId?: string;
  consumoKwh?: string;
};

export type OfertaNormalizada = {
  solucao: "GD" | "Mercado Livre";
  custoKwh: number;
  fornecedor: {
    id: number;
    nome: string;
    numeroClientes: number;
    avaliacaoMedia: number;
    logoUrl: string;
  };
};
