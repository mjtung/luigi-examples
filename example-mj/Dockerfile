# FROM nginx
# COPY nginx.conf /etc/nginx/conf.d/default.conf

FROM continuumio/miniconda3:4.8.2-alpine
COPY src /app
# COPY --from=0 /etc/nginx /etc/nginx
# 10-listen-on-ipv6-by-default.sh
# COPY --from=0 /docker-entrypoint.d/ /docker-entrypoint.d/
# COPY --from=0 /docker-entrypoint.sh /docker-entrypoint.sh
# COPY requirements.txt /app/.
COPY env.yml app/env.yml
COPY run.sh app/run.sh
WORKDIR /app
# RUN conda install --file requirements.txt
ENV PATH /opt/conda/bin:$PATH
RUN conda env update --file env.yml
# RUN chmod +x /docker-entrypoint.sh
# ENTRYPOINT ["/docker-entrypoint.sh"]

# CMD ["nginx", "-g", "daemon off;"]

# CMD conda activate luigi-env
# ENTRYPOINT ["conda", "run", "-n", "luigi-env", "python", "FactorCalculatorTask.py", "FactorCalculatorTask"]
ENTRYPOINT /app/run.sh

