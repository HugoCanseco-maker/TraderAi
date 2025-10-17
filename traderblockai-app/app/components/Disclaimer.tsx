import React from 'react'
import { Alert, AlertDescription } from './ui/alert'
import { AlertTriangle } from 'lucide-react'

const Disclaimer: React.FC = () => {
  return (
    <Alert className="border-orange-200 bg-orange-50 dark:border-orange-800 dark:bg-orange-950">
      <AlertTriangle className="h-4 w-4 text-orange-600 dark:text-orange-400" />
      <AlertDescription className="text-orange-800 dark:text-orange-200 font-medium">
        <strong>Important Legal Notice:</strong> This is a technology demonstration using statistical modeling and is for educational purposes only. 
        <strong className="text-red-600 dark:text-red-400"> This is not financial advice.</strong> All investment decisions should be made with the help of a qualified financial professional.
      </AlertDescription>
    </Alert>
  )
}

export default Disclaimer
