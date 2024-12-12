import pandas as pd

toyota_manual_content_path = 'database/source_documents/toyota_manual.csv'

toyota_parts_book_content_path_xlsx = 'database/source_documents/toyota_parts_book_sample.xlsx'
toyota_parts_book_content_path = 'database/source_documents/toyota_parts_book_sample.csv'

doosan_manual_content_path = 'database/source_documents/doosan_manual.csv'
doosan_manual_content_path_new = 'database/doosan_manual.csv'
doosan_parts_book_content_path = 'database/source_documents/doosan_parts_book.csv'
doosan_parts_book_content_path_new = 'database/doosan_parts_book.csv'


maintenance_sample_content_path = 'database/sample_data.csv'

# NOTE :: CSV/XLSX File Loader
df = pd.read_csv(doosan_parts_book_content_path)
# df = pd.read_excel(toyota_parts_book_content_path)

# # NOTE :: Update CSV File Column sequence 
# df = df[['document_id', 'brand_name', 'model_name', 'knowledge_type', 'file_name', 'page_number', 'title', 'parts_name', 'parts_number', 'page_content']]

# # NOTE :: COPY CSV File Column 
# df['title'] = df['error_code']

# # NOTE :: Column data revision
# df['parts_name'] = df['parts_name'].str.replace('_도면|_세부 부품 목록', '', regex=True)

# # NOTE :: Tuple 순서 정렬
# df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
# df_sorted = df.sort_values('created_at')

# # NOTE :: Frontend constant print
# parts_names = df['parts_name'].unique()
# print("export const doosanPartsNameOptions = [")
# for name in parts_names:
#    print(f"  {{ value: \"{name}\", label: \"{name}\" }},")
# print("]")

# NOTE :: Backend MultiTurn extraction word
parts_names = df['parts_name'].unique()
print("(", end="")
for i, name in enumerate(parts_names):
    if i == len(parts_names) - 1:
        print(f'"{name}"', end="")
    else:
        print(f'"{name}", ', end="")
print(")")


# # NOTE :: Save CSV File
# df.to_csv(doosan_parts_book_content_path, index=False)