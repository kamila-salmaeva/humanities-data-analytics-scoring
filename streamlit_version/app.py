"""Веб-интерфейс скоринговой модели."""
# Этот файл требует model.py и Streamlit-сервер.
# Рабочее приложение — index.html

import streamlit as st

from model import (
    GOALS_MAP,
    LANG_MAP,
    PSYCHO_MAP,
    TIME_MAP,
    get_verdict,
)


def main() -> None:
    """Основная функция приложения."""
    st.set_page_config(
        page_title=(
            "Тест на совместимость: гуманитарный склад ума "
            "и аналитика данных"
        ),
        page_icon="🎓",
    )

    st.title("Из гуманитария в аналитика данных: честный прогноз выживаемости")
    st.markdown(
        "Шутливый тест на нейропластичность. Ответь на 5 вопросов "
        "и узнай свои шансы.",
    )

    psycho = st.selectbox(
        "Что чаще всего приходит в голову при упоминании сложного курса?",
        list(PSYCHO_MAP.keys()),
        key="psycho",
    )

    time = st.selectbox(
        "Сколько часов в неделю ты реально можешь выделить на учебу?",
        list(TIME_MAP.keys()),
        key="time",
    )

    goals = st.selectbox(
        "Твой настрой:",
        list(GOALS_MAP.keys()),
        key="goals",
    )

    lang = st.selectbox(
        "Сколько иностранных языков ты знаешь (хотя бы на уровне "
        "«могу заказать пиццу и понять ответ»)?",
        list(LANG_MAP.keys()),
        key="lang",
    )

    school = st.selectbox(
        "Ты окончила один из топ-3 вузов страны? Ориентируемся на "
        "главные гуманитарные центры из рейтингов RAEX-100 за 2026 "
        "год и «Интерфакс»: МГУ им. М.В. Ломоносова, СПбГУ, НИУ ВШЭ",
        ["Нет", "Да"],
        key="school",
    )

    if st.button("Снять розовые очки"):
        p_psycho = PSYCHO_MAP[psycho]
        p_time = TIME_MAP[time]
        p_goals = GOALS_MAP[goals]
        p_lang = LANG_MAP[lang]

        prob = p_psycho * p_time * p_goals * p_lang
        if school == "Да":
            prob *= 1.1
        prob = min(prob, 1.0)

        st.progress(prob)
        st.metric("Вероятность успеха", f"{prob:.0%}")

        verdict = get_verdict(prob)
        st.markdown(f"### {verdict}")

        st.caption(
            "Модель носит развлекательный характер, не претендует на "
            "научную точность и не применяется для реального отбора. "
            "Все совпадения с шуточными типажами случайны. Проект "
            "создан ради демонстрации архитектурных решений, "
            "вероятностного мышления и чувства юмора автора.",
        )

        if st.button("Не верю! Хочу видеть, что вы другим сказали!"):
            st.rerun()


if __name__ == "__main__":
    main()