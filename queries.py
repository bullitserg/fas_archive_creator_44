get_requests_data_query = '''SELECT
  rd.type AS docType,
  r.ordinalNumber AS rNum,
  IFNULL(rd.documentType, rd.type) AS rDocType,
  CONCAT(rd.id, '_', rd.realName) AS docName,
  rd.uri
FROM procedureRequest r
  JOIN procedures p
    ON p.id = r.procedureId
  JOIN procedureRequestDocument rd
    ON rd.requestId = r.id
WHERE p.registrationNumber = '%(procedure_number)s'
AND r.actualId IS NULL
AND r.requestStatusId != 19
;'''


get_protocols_data_query = '''SELECT
  'protocol' AS docType,
  pd.type AS pDocType,
  CONCAT(pd.id, '_', pd.realName) AS docName,
  pd.uri
FROM procedures p
  JOIN procedureProtocol p1
    ON p1.procedureId = p.id
    AND p1.actualId IS NULL
    AND p1.status = 24
  JOIN procedureProtocolDocument pd
    ON pd.protocolId = p1.id
WHERE p.registrationNumber = '%(procedure_number)s'
AND p.actualId IS NULL;'''


get_features_data_query = '''SELECT
  'explanation' AS docType,
  CONCAT(ed.id, '_', ed.realName) AS docName,
  ed.uri
FROM procedures p
  JOIN procedureExplanation e
    ON e.procedureId = p.id
  JOIN procedureExplanationDocument ed
    ON ed.explanationId = e.id
WHERE p.registrationNumber = '%(procedure_number)s'
AND e.discriminator = 'request'
AND p.actualId IS NULL;'''


get_explanations_data_query = '''SELECT
  'features' AS docType,
  r.ordinalNumber AS rNum,
  CONCAT(rfd.id, '_', rfd.realName) AS docName,
  rfd.uri
FROM procedures p
  JOIN procedureRequest r
    ON r.procedureId = p.id AND r.actualId IS NULL AND r.requestStatusId != 19
  JOIN procedureRequestFeature rf
    ON r.id = rf.requestId
  JOIN procedureRequestFeatureDocument rfd
    ON rfd.requestFeatureId = rf.id
WHERE p.registrationNumber = '%(procedure_number)s'
AND p.actualId IS NULL;'''


get_organisation_data_query = '''SELECT
  'organizationDocument' AS docType,
  CONCAT('organizationDocument_', d.typeId) AS  pDocType,
  r.ordinalNumber AS requestOrdinalNumber,
  CONCAT(d.id, '_', d.realName) AS docName,
  d.uri
FROM procedures p
  JOIN procedureRequest r
    ON r.procedureId = p.id AND r.requestStatusId != 19
  JOIN organization o ON o.id = r.organizationId AND o.actualId IS NULL
  JOIN organizationDocument d ON d.organizationId = o.id
WHERE p.registrationNumber = '%(procedure_number)s'
AND p.actualId IS NULL;
'''


get_offers_data_query = '''SELECT
  r.id AS 'Номер заявки участника',
  org.fullName AS 'Наименование участника',
  org.inn AS 'ИНН',
  IFNULL(ABS(o.offer),'') AS 'Предложенная цена, руб.',
  IF(o.offer IS NOT NULL,IF(o.offer>0,'На понижение v','На повышение ^'),'') AS 'Тип ценового предложения',
  IFNULL(o.createDateTime,'') AS 'Дата и время подачи предложения',
  IF(o.valid=1,'+','') AS 'C учетом шага цены'
FROM procedures p
  JOIN procedureRequest r
    ON r.procedureId = p.id AND r.actualId IS NULL AND r.requestStatusId != 19
  JOIN organization org
    ON org.id = r.organizationId AND org.actualId IS NULL
  JOIN procedureOffer o
    ON o.procedureId = p.id AND o.requestId = r.id
WHERE p.registrationNumber = '%(procedure_number)s'
ORDER BY p.registrationNumber, o.number DESC
;'''
