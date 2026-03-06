import { Button } from 'primereact/button'
import { Card } from 'primereact/card'

export default function App() {
  return (
    <div style={{ padding: '2rem' }}>
      <Card title="PrimeReact funcionando ✅">
        <Button label="Hola PrimeReact" icon="pi pi-check" />
      </Card>
    </div>
  )
}