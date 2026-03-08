import { useRef, useState } from 'react'
import { Toast } from 'primereact/toast'
import { DataTable } from 'primereact/datatable'
import { Column } from 'primereact/column'
import { FileUpload } from 'primereact/fileupload'
import { ProgressBar } from 'primereact/progressbar'
import { Button } from 'primereact/button'
import { InputText } from 'primereact/inputtext'
import { Tooltip } from 'primereact/tooltip'
import { Tag } from 'primereact/tag'
import './App.css'

export default function App() {
  const toast = useRef(null)
  const fileUploadRef = useRef(null)
  const [totalSize, setTotalSize] = useState(0)
  const [uploadKey, setUploadKey] = useState(0)
  const [darkMode, setDarkMode] = useState(false)
  const [variables, setVariables] = useState([])
  const nextIdRef = useRef(1)
  const [editingId, setEditingId] = useState(null)
  const [editName, setEditName] = useState('')
  const [editValue, setEditValue] = useState('')

  const deleteVariable = (id) => {
    setVariables((prev) => prev.filter((v) => v.id !== id))
    if (editingId === id) setEditingId(null)
  }

  const startEdit = (row) => {
    setEditingId(row.id)
    setEditName(row.name)
    setEditValue(row.value)
  }

  const saveEdit = () => {
    if (editingId == null) return
    setVariables((prev) =>
      prev.map((v) =>
        v.id === editingId ? { ...v, name: editName, value: editValue } : v
      )
    )
    setEditingId(null)
  }

  const cancelEdit = () => {
    setEditingId(null)
  }

  const toggleTheme = () => {
    const theme = darkMode ? 'lara-light-blue' : 'lara-dark-blue'
    const link = document.getElementById('theme-link')
    if (link) link.href = `/node_modules/primereact/resources/themes/${theme}/theme.css`
    setDarkMode(!darkMode)
  }

  const triggerFileSelect = () => {
    const inputs = document.querySelectorAll('input[type="file"]')
    if (inputs.length > 0) inputs[0].click()
  }

  const onTemplateSelect = (e) => {
    let _totalSize = 0
    Object.keys(e.files).forEach((key) => { _totalSize += e.files[key].size || 0 })
    setTotalSize(_totalSize)
  }

  const onTemplateUpload = (e) => {
    const xhr = e?.xhr
    const raw = xhr?.responseText ?? xhr?.response
    if (raw) {
      try {
        const data = JSON.parse(raw)
        if (Array.isArray(data?.metadata)) {
          const list = data.metadata.map((item, i) => ({
            id: nextIdRef.current + i,
            name: String(item.tag ?? ''),
            value: String(item.value ?? '')
          }))
          nextIdRef.current += list.length
          setVariables(list)
          setEditingId(null)
        }
      } catch (_) { /* ignore parse error */ }
    }
    toast.current?.show({ severity: 'success', summary: 'Listo', detail: 'Imagen subida. Metadatos cargados en la tabla.' })
    setTotalSize(0)
    setUploadKey((k) => k + 1)
    setTimeout(() => fileUploadRef.current?.clear(), 50)
  }

  const onTemplateRemove = (file, callback) => {
    setTotalSize((prev) => prev - (file.size || 0))
    callback()
  }

  const onTemplateClear = () => setTotalSize(0)

  const onUploadError = () => {
    toast.current?.show({ severity: 'error', summary: 'Error', detail: 'No se pudo subir la imagen. Revisa la conexión o el formato.' })
    setTotalSize(0)
  }

  const MAX_UPLOAD_BYTES = 500000000
  const headerTemplate = (options) => {
  const { className, chooseButton, cancelButton } = options
  const value = Math.min(100, (totalSize / MAX_UPLOAD_BYTES) * 100)
  const formatedValue = fileUploadRef?.current?.formatSize
    ? fileUploadRef.current.formatSize(totalSize)
    : '0 B'
  const isNearLimit = value >= 80

  return (
    <div className={className} style={{ backgroundColor: 'transparent', display: 'flex', alignItems: 'center', minHeight: '58px' }}>
      <div style={{ opacity: totalSize > 0 ? 1 : 0, pointerEvents: totalSize > 0 ? 'auto' : 'none', width: '42px' }}>
        {chooseButton}
      </div>
      {cancelButton}
      <div className="flex align-items-center gap-3 ml-auto">
        <span style={{ color: isNearLimit ? '#ef4444' : 'inherit' }}>{formatedValue} / 500 MB</span>
        <ProgressBar value={value} showValue={false}
          style={{ width: '10rem', height: '12px' }}
          color={isNearLimit ? '#ef4444' : '#38bdf8'} />
      </div>
    </div>
  )
}

  const itemTemplate = (file, props) => (
    <div className="gallery-item">
      <img alt={file.name} role="presentation" src={file.objectURL} />
      <div className="gallery-item-info">
        <span className="gallery-item-name">{file.name}</span>
        <small>{new Date().toLocaleDateString()}</small>
        <div className="gallery-item-footer">
          <Tag value={typeof props.formatSize === 'function' ? props.formatSize(file.size) : ''} severity="info" />
          <Button type="button" icon="pi pi-times"
            className="p-button-outlined p-button-rounded p-button-danger"
            onClick={() => onTemplateRemove(file, props.onRemove)} />
        </div>
      </div>
    </div>
  )

  const emptyTemplate = () => (
    <div className="empty-drop-area" onClick={triggerFileSelect}>
      <i className="pi pi-image" />
      <span>Arrastra tus archivos aquí o haz clic para seleccionar</span>
    </div>
  )

  const chooseOptions = {
    icon: 'pi pi-fw pi-images',
    iconOnly: true,
    className: 'custom-choose-btn p-button-rounded p-button-outlined',
  }
  const uploadOptions = { style: { display: 'none' } }
  const cancelOptions = { style: { display: 'none' } }

  return (
    <div className="page">
      <Toast ref={toast} />
      <Tooltip target=".custom-choose-btn" content="Agregar más" position="bottom" />

      <button className="theme-toggle" onClick={toggleTheme}>
        <i className={`pi ${darkMode ? 'pi-sun' : 'pi-moon'}`} />
      </button>

      <h1 className="title">DataView</h1>

      <div className="upload-wrapper">
        <FileUpload
          key={uploadKey}
          ref={fileUploadRef}
          name="file"
          url="/api/upload"
          accept="image/*"
          maxFileSize={500000000}
          onUpload={onTemplateUpload}
          onSelect={onTemplateSelect}
          onError={onUploadError}
          onClear={onTemplateClear}
          headerTemplate={headerTemplate}
          itemTemplate={itemTemplate}
          emptyTemplate={emptyTemplate}
          chooseOptions={chooseOptions}
          uploadOptions={uploadOptions}
          cancelOptions={cancelOptions}
        />
      </div>

      <div className="action-buttons">
        <Button
          label="Cargar"
          onClick={() => fileUploadRef.current?.upload()}
          disabled={totalSize === 0}
        />
        <Button
          label="Limpiar"
          className="p-button-outlined p-button-secondary"
          onClick={() => { setTotalSize(0); setUploadKey((k) => k + 1) }}
          disabled={totalSize === 0}
        />
      </div>

      <div className="variables-section">
        <h2 className="variables-title">Variables</h2>
        <div className="variables-table-wrapper">
          <DataTable
            value={variables}
            dataKey="id"
            size="small"
            stripedRows
            responsiveLayout="stack"
            emptyMessage="No hay variables. Sube una imagen para cargar sus metadatos."
            className="variables-datatable"
          >
            <Column
              header="Nombre variable"
              body={(row) =>
                editingId === row.id ? (
                  <InputText
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                    className="variable-edit-input"
                  />
                ) : (
                  <span>{row.name}</span>
                )
              }
            />
            <Column
              header="Variable"
              body={(row) =>
                editingId === row.id ? (
                  <InputText
                    value={editValue}
                    onChange={(e) => setEditValue(e.target.value)}
                    className="variable-edit-input"
                  />
                ) : (
                  <span>{row.value}</span>
                )
              }
            />
            <Column
              header="Acciones"
              body={(row) => (
                <div className="variable-actions">
                  {editingId === row.id ? (
                    <>
                      <Button
                        icon="pi pi-check"
                        className="p-button-rounded p-button-text p-button-success"
                        tooltip="Guardar"
                        tooltipOptions={{ position: 'top' }}
                        onClick={saveEdit}
                      />
                      <Button
                        icon="pi pi-times"
                        className="p-button-rounded p-button-text p-button-secondary"
                        tooltip="Cancelar"
                        tooltipOptions={{ position: 'top' }}
                        onClick={cancelEdit}
                      />
                    </>
                  ) : (
                    <>
                      <Button
                        icon="pi pi-pencil"
                        className="p-button-rounded p-button-text p-button-secondary"
                        tooltip="Editar"
                        tooltipOptions={{ position: 'top' }}
                        onClick={() => startEdit(row)}
                      />
                      <Button
                        icon="pi pi-trash"
                        className="p-button-rounded p-button-text p-button-danger"
                        tooltip="Eliminar"
                        tooltipOptions={{ position: 'top' }}
                        onClick={() => deleteVariable(row.id)}
                      />
                    </>
                  )}
                </div>
              )}
            />
          </DataTable>
        </div>
      </div>
    </div>
  )
}