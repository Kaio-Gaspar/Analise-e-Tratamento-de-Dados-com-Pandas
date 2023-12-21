import pandas as pd
import os
import matplotlib.pyplot as plt 
# csv e xlsx para dataframe
cadastro_clientes_df = pd.read_csv('CadastroClientes.csv', sep=';', decimal=',')
cadastro_funcionarios_df = pd.read_csv('CadastroFuncionarios.csv', sep=';', decimal=',')
servicos_prestados_df = pd.read_excel('BaseServiçosPrestados.xlsx')

# calcular total de salario imposto e beneficio

# converte o impoto para float e soma todos os itens da coluna
imposto_funcionario = cadastro_funcionarios_df['Impostos'].astype(float).sum()
# soma tod salario dos funcionarios
salario_funcionario = cadastro_funcionarios_df['Salario Base'].astype(float).sum()
#  soma tofo beneficio em $ dos funcionarios
beneficio_funcionario = cadastro_funcionarios_df['Beneficios'].astype(float).sum()
# soma o vt e vr
valor_vt_mais_vr_funcionarios = cadastro_funcionarios_df['VT'].sum().astype(int) + cadastro_funcionarios_df['VR'].sum().astype(int)
# soma folha
valor_total_da_folha_salarial = imposto_funcionario + salario_funcionario + beneficio_funcionario + valor_vt_mais_vr_funcionarios
# cria coluna da folha salaria de cada funcionario
cadastro_funcionarios_df['Salario Total'] = cadastro_funcionarios_df['Beneficios'] + cadastro_funcionarios_df['Impostos'] + cadastro_funcionarios_df['Salario Base'] + cadastro_funcionarios_df['VR'] + cadastro_funcionarios_df['VT']

print('----------------------------------')
print(f' O total de imposto dos funcionarios é R${imposto_funcionario:,} .\n O total de salario base é R${salario_funcionario:,} .\n O total gasto em beneficios para os funcionario é R${beneficio_funcionario:,} .\n O total gasto com VT e VR é de R${valor_vt_mais_vr_funcionarios:,}.')
print(f' O valor total da folha salarial pago pela empresa é de R${valor_total_da_folha_salarial:,} .')
print('----------------------------------')
print(cadastro_funcionarios_df)
print('----------------------------------')
# cria uma tabela 
faturamento_df = servicos_prestados_df[['ID Cliente',  'Tempo Total de Contrato (Meses)']].merge(cadastro_clientes_df[['ID Cliente', 'Valor Contrato Mensal']])
# cria coluna de faturamento
faturamento_df['Faturamento'] = faturamento_df['Tempo Total de Contrato (Meses)'] * faturamento_df['Valor Contrato Mensal']
# soma o faturamento totla
faturamento_total = faturamento_df['Faturamento'].sum()

print(faturamento_df)
print(f'O faturamento total da empresa é R${faturamento_total:,}')

# calcula a % de servicos fechados por total de funcionarios
quantidade_de_funcionario_que_fecharam_servico = len(servicos_prestados_df['ID Funcionário'].unique())
quantidade_funcionarios = len(cadastro_funcionarios_df['ID Funcionário'].unique())

print(f'A porcentagem de funcionarios que fecharam contrato é de {(quantidade_de_funcionario_que_fecharam_servico/quantidade_funcionarios):.2%}\n')
print('----------------------------------')

# cria tabela com cada area e junta as area para serem unicas, contando os serviçoes feitos
contratos_por_area = cadastro_funcionarios_df[['Area', 'ID Funcionário']].merge(servicos_prestados_df[['ID Funcionário']], on='ID Funcionário')
print('Tabela de serviços realizado por cada area')
contratos_por_area = contratos_por_area.groupby('Area').count().reset_index()


print(contratos_por_area)
print('----------------------------------')
# cria uma tabela grafica com matplotlib
funcionario_por_area = cadastro_funcionarios_df['Area'].value_counts()
funcionario_por_area.plot(kind='pie', autopct='%1.1f%%', startangle=90, figsize=(8, 8))
plt.title('Distribuição de Funcionários por Área')
plt.ylabel('')  
plt.xlabel('')

# calcula media do ticket medio
ticket_medio = cadastro_clientes_df['Valor Contrato Mensal'].mean()
print(f'O ticket mensal foi de R${ticket_medio:,.2f}')
plt.show()
