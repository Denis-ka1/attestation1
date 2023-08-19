import pandas as pd
import streamlit as sl
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
import statsmodels.api as sm

uploaded_file = sl.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df1 = pd.DataFrame({ 'category': list(df) })

    col1, col2 = sl.columns(2)
    with col1:
        option1 = sl.selectbox( 'Параметр 1', (list(df)))
    
    with col2:
        option2 = sl.selectbox( 'Параметр 2', (list(df)))

    categrial = sl.checkbox("Категориальная")

    

    if categrial:
        Kategorial_df =  df[[option1, option2]].groupby(option1).sum().sort_values(option2, ascending=False)
        labels = list(Kategorial_df.T)
        data = list(Kategorial_df[option2])
        data_percent = list(map(lambda x: x/sum(data)*100, data))
        fig, ax = plt.subplots()
        ax.pie(data_percent, labels=labels)
        sl.pyplot(fig)

    else:
        data2 = [df[option1], df[option2]]
        fig, ax = plt.subplots()
        ax.hist(data2)
        sl.pyplot(fig)

    Test = sl.selectbox( 'Выбор алгоритма', [ "mannwhitneyu", 't-test'])

    if Test == "mannwhitneyu":
        _, pnorm = mannwhitneyu(df[option1], df[option2], use_continuity=False,
                            method="asymptotic")
        sl.write(pnorm)
    
    else:
        tstat, pvalue, df = sm.stats.ttest_ind(
        df[option1],
        df[option2],
        usevar='unequal', alternative='smaller')
        sl.write(f'p-value: {pvalue:.4f}')
