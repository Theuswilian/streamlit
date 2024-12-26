import streamlit as st
from datetime import datetime, timedelta
import time

# Página inicial
st.title("Savia - Gerenciador de Rotinas")
st.write("Organize sua rotina e seja mais produtivo!")

# Lista de tarefas
tasks = []

# Formulário para adicionar tarefas
st.subheader("Adicione uma nova tarefa:")
task_name = st.text_input("Nome da Tarefa", key="task_name")
task_time = st.time_input("Horário da Tarefa", key="task_time")

if st.button("Adicionar Tarefa"):
    task_datetime = datetime.combine(datetime.today(), task_time)
    tasks.append({"nome": task_name, "horario": task_datetime})
    st.success("Tarefa adicionada com sucesso!")

# Exibir tarefas na rotina
st.subheader("Sua Rotina:")
if tasks:
    for task in sorted(tasks, key=lambda x: x["horario"]):
        st.write(f"- {task['nome']} às {task['horario'].strftime('%H:%M')}")
else:
    st.write("Nenhuma tarefa adicionada ainda.")

# Função para alertar tarefas próximas
st.subheader("Alertas de Tarefas:")
current_time = datetime.now()
for task in tasks:
    time_difference = task["horario"] - current_time
    if 0 < time_difference.total_seconds() <= 1200:  # Alertar para tarefas dentro de 20 minutos
        st.warning(f"Tarefa próxima: {task['nome']} às {task['horario'].strftime('%H:%M')}!")

# Rodar alertas no console (exemplo básico)
def run_alerts():
    while True:
        now = datetime.now()
        for task in tasks:
            if task["horario"].strftime('%H:%M') == now.strftime('%H:%M'):
                print(f"🔔 Alerta! Hora de: {task['nome']}")
        time.sleep(60)

if st.button("Iniciar Alertas"):
    st.write("Monitorando tarefas... Verifique alertas no console!")
    run_alerts()
