from typing import List

import langchain
from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent_toolkits import VectorStoreInfo, VectorStoreToolkit
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, UnstructuredHTMLLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.tools import BaseTool

langchain.verbose = True


# Index作成
def create_index() -> VectorStoreIndexWrapper:
    '''
    loader = DirectoryLoader("./src/", glob="**/*.txt") # フォルダ内のテキストをすべて学習させる場合
    loader = PyPDFLoader("./src/pdzac.pdf") # Vectorソースの指定
    '''
    loader = DirectoryLoader("./src/JP2_html_201020_2/", glob="**/*.html", loader_cls=UnstructuredHTMLLoader) # フォルダ内のHTMLをすべて学習させる場合
    return VectorstoreIndexCreator().from_loaders([loader]) # リストでloaderを返す


# langChain - Vector Store Agentより
## VectorStoreIndexWrapperのtool化
def create_tools(index: VectorStoreIndexWrapper) -> List[BaseTool]:
    vectorstore_info = VectorStoreInfo(
        vectorstore=index.vectorstore,
        name="udemy-langchain source code",
        description="Source code of application named udemy-langchain",
    )
    toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
    return toolkit.get_tools()


# gpt-3.5-turbo APIを使用
## https://openai.com/pricing
def chat(
    message: str, history: ChatMessageHistory, index: VectorStoreIndexWrapper
) -> str:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0,) # llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    tools = create_tools(index)

    # 上記のhistoryを渡して初期化
    memory = ConversationBufferMemory(
        chat_memory=history, memory_key="chat_history", return_messages=True
    )

    # LangChain - Conversation Agent (for Chatmodels)より
    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        handle_parsing_errors="Check your output and make sure it conforms!" # gpt-3.5-turbo使用時のパースエラー対策
    )

    return agent_chain.run(input=message)
