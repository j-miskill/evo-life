# def trigger_inference(form_data):
#     # Generate encoded and phenotype data (mocked here)
#     encoded_genes = {"encoded_nremhr": 67.2, "encoded_rmssd": 39.8}
#     decoded_phenotype = "Healthy"

#     # Append to MySQL
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     insert_query = """
#     INSERT INTO encoded_health_metrics (encoding_id, metric_id, encoded_nremhr, encoded_rmssd, ...)
#     VALUES (%s, %s, %s, %s, ...)
#     """
#     cursor.execute(insert_query, ("E<metric_id>", "<metric_id>", 67.2, 39.8))
#     conn.commit()
#     conn.close()

#     return {
#         "original_metrics": form_data,
#         "encoded_genes": encoded_genes,
#         "predicted_phenotype": decoded_phenotype
#     }