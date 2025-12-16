import streamlit as st

# =====================================
# ページ設定
# =====================================
st.set_page_config(
    page_title="SME SBT 要件チェック",
    layout="wide"
)

# =====================================
# CSS
# =====================================
st.markdown("""
<style>
h1 { font-size:32px; margin-bottom:0.6rem; }
[data-testid="stMarkdownContainer"] h2 {
    font-size:15px; font-weight:600;
    margin-top:1.2rem; margin-bottom:0.3rem;
}
[data-testid="stSubheader"] h3,
[data-testid="stMarkdownContainer"] h3 {
    font-size:15px; font-weight:400;
    margin-top:0.3rem; margin-bottom:0.4rem;
}
label { font-size:15px; }
.stCaption { font-size:13px; color:#666; line-height:1.4; }
pre code { font-size:13px; }
.block-container { padding:2rem; }
</style>
""", unsafe_allow_html=True)

# =====================================
# タイトル
# =====================================
st.title("SME SBT 要件チェック")

# =====================================
# 要件①（4項目すべて必須）
# =====================================
st.markdown("## 要件①：以下4項目すべてを満たす必要あり")

st.subheader("① 排出量要件（Scope1 + Scope2）")
st.caption(
    "Scope1 と Scope2（ロケーション基準）の合計排出量が "
    "10,000 t-CO₂e 未満である必要があります。"
)
emissions_result = st.radio(
    "Scope1とロケーション基準Scope2の合計排出量",
    ["10,000 t-CO₂e 未満", "10,000 t-CO₂e 以上"],
    horizontal=True
)

st.subheader("② セクター要件")
st.caption(
    "金融機関・石油・ガスセクターとは、\n"
    "① 投融資により本業を超える事業を行っている場合\n"
    "② 石油・ガス（採掘、輸送、販売等）からの収益が大半を占める場合\n"
    "を指します。"
)
sector_result = st.radio(
    "金融機関・石油・ガスに該当しますか",
    ["該当しない", "該当する"],
    horizontal=True
)

st.subheader("③ 追加目標設定が必要な業種")
st.caption(
    "石油・ガス、電力、鉄鋼、セメント、航空、海運、農業、森林など、\n"
    "① 製造過程で CO₂ が化学的に発生する\n"
    "② 極めて高温の熱源や大量の電力を恒常的に使用する\n"
    "事業が該当します。"
)
excluded_industry = st.radio(
    "該当しますか",
    ["該当しない", "該当する"],
    horizontal=True
)

st.subheader("④ 親会社・関連会社の確認")
st.caption(
    "SME SBT では「自社 ≒ 自グループ」という考え方が取られます。\n"
    "親会社・関連会社がある場合、原則としてグループ全体での申請が前提となります。"
)
has_parent = st.radio(
    "親会社または関連会社はありますか",
    ["ない", "ある"],
    horizontal=True
)

group_meets = control_from_others = None
if has_parent == "ある":
    group_meets = st.radio(
        "グループ全体で SME SBT 要件を満たしていますか",
        ["はい", "いいえ", "未確認"],
        horizontal=True
    )

    st.caption(
        "ここでの「グループ」とは、資本関係や経営支配力を通じて\n"
        "実質的に一体として管理されている範囲を指します。"
    )

    control_from_others = st.radio(
        "関係会社が自社の経営決定権を持っていますか",
        ["いいえ", "はい", "未確認"],
        horizontal=True,
        index=0
    )

    st.caption(
        "「はい」の場合、自社単体ではなく、\n"
        "関係会社を含めたグループとして申請を行う必要があります。"
    )

# =====================================
# 判定①（要件①）
# =====================================
req1_ng = []

if emissions_result == "10,000 t-CO₂e 以上":
    req1_ng.append("排出量が上限を超過している")
if sector_result == "該当する":
    req1_ng.append("金融機関・石油・ガスセクターに該当する")
if excluded_industry == "該当する":
    req1_ng.append("追加目標設定が必要な業種に該当する")

if has_parent == "ある":
    if group_meets != "はい":
        req1_ng.append("グループ全体での要件が未確認または未充足")
    if control_from_others != "いいえ":
        req1_ng.append("関係会社が自社の経営決定権を持っている")

status_req1 = "OK" if not req1_ng else "NG"

st.subheader("判定（要件①）")
if status_req1 == "OK":
    st.success("OK")
else:
    st.error("NG")
    for r in req1_ng:
        st.write("・", r)

# =====================================
# 要件②（4項目中3項目以上）
# =====================================
st.markdown("## 要件②：以下4項目中3項目以上を満たす必要あり")

employee_ok = st.radio(
    "従業員数（250人未満）に該当しますか",
    ["該当しない", "該当する"],
    horizontal=True
)

revenue_ok = st.radio(
    "売上高（5,000万ユーロ未満）に該当しますか",
    ["該当しない", "該当する"],
    horizontal=True
)

assets_ok = st.radio(
    "総資産（2,500万ユーロ未満）に該当しますか",
    ["該当しない", "該当する"],
    horizontal=True
)

flag_business = st.radio(
    "大規模な森林・土地開発・農業事業に該当しますか",
    ["該当しない", "該当する"],
    horizontal=True
)

st.caption(
    "大規模の目安：当該事業に起因する排出量が、\n"
    "自社（グループ）全体の排出量の 20% を超える場合を指します。"
)

score_req2 = sum([
    employee_ok == "該当しない",
    revenue_ok == "該当しない",
    assets_ok == "該当しない",
    flag_business == "該当しない"
])
status_req2 = "OK" if score_req2 >= 3 else "NG"

req2_ng = []
if employee_ok == "該当する":
    req2_ng.append("従業員数が要件超過")
if revenue_ok == "該当する":
    req2_ng.append("売上高が要件超過")
if assets_ok == "該当する":
    req2_ng.append("総資産が要件超過")
if flag_business == "該当する":
    req2_ng.append("森林・土地開発・農業事業に該当")

# =====================================
# 判定②・最終判定
# =====================================
has_unconfirmed = "未確認" in [group_meets, control_from_others]

if has_unconfirmed:
    final_status = "保留"
elif status_req1 == "OK" and status_req2 == "OK":
    final_status = "申請可能"
else:
    final_status = "申請不可"

st.subheader("判定（要件②）")
if status_req2 == "OK":
    st.success("OK")
else:
    st.error("NG")
    for r in req2_ng:
        st.write("・", r)

st.subheader("最終判定（申請可否）")
if final_status == "申請可能":
    st.success("申請可能")
elif final_status == "申請不可":
    st.error("申請不可")
else:
    st.warning("保留")

# =====================================
# ⑥〜⑧ 参考情報（順序変更）
# =====================================
st.subheader("⑥ 申請費用")
fee_revenue = st.radio(
    "売上高区分",
    ["年間売上高 500万ユーロ未満", "年間売上高 500万ユーロ以上"],
    horizontal=True
)
fee_amount = "USD 1,250" if "未満" in fee_revenue else "USD 2,000"
st.info(f"想定申請費用：{fee_amount}")

st.markdown("---")
st.subheader("⑦ 排出源（確認）")
emission_sources = st.multiselect(
    "排出源",
    ["ガス（都市ガス）", "ガス（LPG）", "ガソリン", "軽油", "重油", "電気", "その他"]
)

other_emission_source = ""
if "その他" in emission_sources:
    other_emission_source = st.text_input("その他の排出源（自由記述）")

st.subheader("⑧ 拠点（確認）")
has_sites = st.radio("拠点の有無", ["なし", "ある"], horizontal=True)
site_details = ""
if has_sites == "ある":
    site_details = st.text_input("拠点名")

# =====================================
# コピー用まとめ
# =====================================
st.markdown("---")
st.subheader("入力内容まとめ（クリックでコピー）")

normal_sources = [s for s in emission_sources if s != "その他"]

if normal_sources and "その他" in emission_sources and other_emission_source:
    emission_text = ", ".join(normal_sources + [other_emission_source])
elif normal_sources:
    emission_text = ", ".join(normal_sources)
elif "その他" in emission_sources and other_emission_source:
    emission_text = other_emission_source
else:
    emission_text = "未選択"

summary_text = f"""
【SME SBT 要件チェック 入力内容】

要件①（4項目すべて必須）
- 排出量要件：{"該当しない" if emissions_result == "10,000 t-CO₂e 未満" else "該当する"}
- セクター要件：{sector_result}
- 追加目標設定が必要な業種：{excluded_industry}
- 親会社・関連会社：{"該当しない" if has_parent == "ない" else "該当する"}

要件②（4項目中3項目以上）
- 従業員数：{employee_ok}
- 売上高：{revenue_ok}
- 総資産：{assets_ok}
- 森林・土地開発・農業事業：{flag_business}

確認情報
- 申請費用：{fee_amount}
- 排出源：{emission_text}
- 拠点：{has_sites}
{"- 拠点名：" + site_details if site_details else ""}

判定結果
- 要件①：{status_req1}
- 要件②：{status_req2}
- 最終判定：{final_status}
""".strip()

st.code(summary_text, language="text")
