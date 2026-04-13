export interface PDFResponse {
  type_contenu: string;
  message: string;
}

export interface ComprehensionResponse {
  conseils: [string]
  prerequis: [string]
  outils: [string]
  temps_estime: number
  warning: [string]
}