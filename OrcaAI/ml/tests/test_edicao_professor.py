"""A edição com permalinks não pode apontar outra execução como evidência."""
import hashlib

import pytest

from orca_ml import edicao_professor as edicao
from orca_ml.relatorio_consolidado import gerar_relatorio_consolidado


def test_manifesto_alterado_nao_recebe_links_da_execucao_publicada(tmp_path, monkeypatch):
    p=tmp_path/'execucao_estudo.json';p.write_bytes(b'original')
    monkeypatch.setattr(edicao,'SHA_EXECUCAO',hashlib.sha256(b'original').hexdigest())
    meta=edicao.conferir_execucao(p)
    assert meta['commit_experimental']==edicao.COMMIT
    p.write_bytes(b'outra execucao')
    out=tmp_path/'relatorio'
    with pytest.raises(ValueError,match='manifesto diverge'):
        gerar_relatorio_consolidado(tmp_path,{},out,edicao=meta)
    assert not out.exists()


def test_links_codificam_caminhos_sem_mudar_commit():
    url=edicao.github('pasta/tabela de preços.csv')
    assert '/blob/'+edicao.COMMIT+'/' in url
    assert url.endswith('pasta/tabela%20de%20pre%C3%A7os.csv')
