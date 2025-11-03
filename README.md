# Photo Syncer - AWS S3 & MySQL Integration

Um sistema automatizado para sincronizar fotos locais com Amazon S3 e atualizar URLs no banco MySQL correspondente.

## 📋 Descrição

Este projeto permite fazer upload em lote de fotos para Amazon S3 e automaticamente atualizar o banco de dados MySQL com as URLs das imagens hospedadas no S3. Ideal para migração de fotos de usuários ou sincronização de perfis de usuário com armazenamento em nuvem.

## 🚀 Funcionalidades

- **Upload automatizado para S3**: Faz upload de múltiplas fotos para um bucket S3
- **Atualização automática do MySQL**: Atualiza a coluna `foto` na tabela `users` com URLs do S3
- **Extração de User ID**: Extrai automaticamente o ID do usuário a partir do nome do arquivo
- **Suporte a SSH Tunnel**: Conecta ao MySQL através de túnel SSH quando necessário
- **Validação de entrada**: Confirma operações antes de executar mudanças no banco
- **Padrões flexíveis**: Suporta diferentes padrões de nomenclatura de arquivos

## 📋 Pré-requisitos

- Python 3.8+
- Conta AWS com acesso ao S3
- Banco de dados MySQL com tabela `users` contendo coluna `foto`
- Credenciais AWS configuradas (via AWS CLI, IAM roles, ou variáveis de ambiente)

## 🛠️ Configuração e Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/nicholasvjo/aws-s3-mysql-photo-syncer.git
cd photo-syncer
```

### 2. Configure o ambiente virtual Python
```bash
# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No macOS/Linux:
source venv/bin/activate
# No Windows:
# venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
# Copie o arquivo de exemplo e configure suas variáveis
cp .env.example .env
```

Edite o arquivo `.env` e substitua os valores pelos seus dados reais:
- **AWS**: Configure suas credenciais AWS via `aws configure` ou variáveis de ambiente
- **MySQL**: Insira os dados de conexão do seu banco de dados
- **SSH Tunnel** (Opcional): Deixe em branco se não precisar. Usado quando o MySQL está em servidor remoto acessível apenas via SSH

> **💡 Dica sobre SSH Tunnel**: Se seu banco MySQL estiver em um servidor remoto que requer acesso via SSH (comum em serviços cloud), preencha as configurações SSH. Caso contrário, deixe essas variáveis vazias para conexão direta.

## 📚 Como usar

### Comando básico
```bash
python src/main.py /caminho/para/fotos
```

### Com padrão personalizado de arquivo
```bash
python src/main.py /caminho/para/fotos --pattern "user_{user_id}_profile.jpg"
```

### Pular confirmação (modo automático)
```bash
python src/main.py /caminho/para/fotos --no-confirm
```

### Testar conexão com banco
```bash
python src/main.py . --test-connection
```

## 📁 Estrutura do Projeto

```
photo-syncer/
├── src/
│   ├── main.py          # Aplicação principal
│   ├── s3.py            # Funções para upload S3
│   ├── my_sql.py        # Operações MySQL
│   ├── config.py        # Configurações e variáveis
│   └── constants.py     # Constantes do projeto
├── requirements.txt     # Dependências Python
└── README.md           # Este arquivo
```

## 🔧 Como funciona

### 1. **Processamento de Arquivos**
O sistema percorre o diretório especificado e:
- Extrai o `user_id` de cada arquivo baseado no padrão fornecido
- Valida se o arquivo é válido e se o ID foi extraído corretamente
- Faz upload do arquivo para S3 com a nomenclatura `{user_id}.jpg`

### 2. **Operações no Banco MySQL**
Para cada upload bem-sucedido:
- Gera uma query SQL dinâmica para atualizar múltiplos usuários
- Executa: `UPDATE users SET foto = CONCAT('https://bucket.s3.region.amazonaws.com/dir/', id, '.jpg') WHERE id IN (...)`
- Atualiza a coluna `foto` com a URL completa da imagem no S3

### 3. **Exemplo de Operação SQL**
```sql
UPDATE users 
SET foto = CONCAT('https://meu-bucket.s3.us-east-1.amazonaws.com/photos/users/', id, '.jpg') 
WHERE id IN (1, 2, 3, 4, 5);
```

## 🛡️ Segurança

- **SSH Tunnel**: Suporte para conexões seguras via túnel SSH
- **Validação de entrada**: Confirmação obrigatória antes de modificar o banco
- **Gerenciamento de conexões**: Context managers para garantir fechamento adequado das conexões
- **ACL S3**: Arquivos enviados com permissão de leitura pública (`public-read`)

## 📊 Exemplo de Uso

Supondo que você tenha arquivos nomeados como:
- `123.jpg`
- `456.jpg` 
- `789.jpg`

O sistema irá:
1. Fazer upload para S3 como: `photos/users/123.jpg`, `photos/users/456.jpg`, etc.
2. Atualizar MySQL: 
   - User ID 123: `foto = 'https://bucket.s3.region.amazonaws.com/photos/users/123.jpg'`
   - User ID 456: `foto = 'https://bucket.s3.region.amazonaws.com/photos/users/456.jpg'`
   - User ID 789: `foto = 'https://bucket.s3.region.amazonaws.com/photos/users/789.jpg'`

## 🎯 Padrões de Arquivo Suportados

- **Padrão padrão**: `{user_id}.jpg` (ex: `123.jpg`)
- **Padrões personalizados**: 
  - `user_{user_id}_photo.jpg` (ex: `user_123_photo.jpg`)
  - `profile_{user_id}.png` (ex: `profile_456.png`)
  - Qualquer padrão que contenha `{user_id}`

## 🔍 Troubleshooting

### Erro de conexão MySQL
```bash
python src/main.py . --test-connection
```

### Verificar configuração AWS
```bash
aws s3 ls s3://seu-bucket-name
```

### Logs detalhados
O sistema fornece logs detalhados para cada operação, incluindo:
- Status de upload para S3
- Número de usuários atualizados no MySQL
- Tempo total de execução
- Erros específicos por arquivo

---

**Desenvolvido por**: [Nicholas Vivacqua Johannesen](https://github.com/nicholasvjo)
