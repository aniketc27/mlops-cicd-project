pipeline {
    agent any

    environment {
        MODEL_DIR = './model'
        PROCESSED_DATA_DIR = './processed_data'
        RESULTS_DIR = './results'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies'
                script {
                    // withPythonEnv('file:///C://Users//91886//AppData//Local//Microsoft//WindowsApps//PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0//python3.exe') {
                    //     bat 'python3 -m pip install -r requirements.txt' || error 'Failed to install dependencies'
                    // }
                    //bat '@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"'
                    //powershell 'Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString("https://chocolatey.org/install.ps1"))'
                    //powershell 'choco install python -y'
                    //powershell 'python --version'
                    def pythonVersion = '3.9.7'
                    
                    def pythonInstallerUrl = '''https://www.python.org/ftp/python/$%7BpythonVersion%7D/python-$%7BpythonVersion%7D-amd64.exe'''
                    def encodedUrl = URLEncoder.encode(pythonInstallerUrl, "UTF-8")
                    // Define Python installation directory
                    def pythonInstallDir = '''${env.USERPROFILE}\AppData\Local\Programs\Python\Python${pythonVersion}'''

                    // Download Python installer
                    bat "curl -o python-${pythonVersion}-amd64.exe ${encodedUrl}"

                    // Install Python
                    bat "python-${pythonVersion}-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0"

                    // Add Python to PATH
                    bat "echo %PATH%"

                    // Verify Python installation
                    bat "python --version"
                }
            }
        }

        stage('Preprocess') {
            steps {
                echo 'Preprocessing'
                script {
                    withPythonEnv('python3') {
                        powershell 'python3 preprocess.py' || error 'Preprocessing failed'
                    }
                }
            }
        }

        stage('Train') {
            steps {
                echo 'Training'
                script {
                    withPythonEnv('python3') {
                        sh 'python3 train.py' || error 'Training failed'
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Testing'
                script {
                    withPythonEnv('python3') {
                        sh 'python3 testing.py' || error 'Testing failed'
                    }
                }
            }
        }
    }

}
