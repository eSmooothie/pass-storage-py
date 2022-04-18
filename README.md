# PASSWORD STORAGE

Store and access your passwords in a fancy way.

The program will store your password information in your device and you can access it through a system command.

### Windows Installation
***
1. Clone the repository.

        git clone https://github.com/eSmooothie/pass-storage-py.git

2. Install [python](https://www.python.org/downloads/).
3. Add a __PYTHON_PATH__ in your system variable. [see for reference](https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-so-it-finds-my-modules-packages) 

4. Add __**\<project_path\>/pass-storage-py/**__ to your system __**PATH**__.
5. Run the command below in the command prompt.

        mypass
***

### Commands

<table style='width:100%;'>
        <thead>
                <tr>
                        <th>Command/Usage</th>
                        <th>Description</th>
                </tr>
        </thead>
        <tbody>
                <tr>
                        <td><code>mypass -h</code></td>
                        <td>Display help</td>
                </tr>
                <tr>
                        <td><code>mypass add</code></td>
                        <td>Add new data</td>
                </tr>
                <tr>
                        <td><code>mypass view -a/--all</code></td>
                        <td>Display all stored data</td>
                </tr>
                <tr>
                        <td><code>mypass view -r/ref [reference]</code></td>
                        <td>Display full detail of the data</td>
                </tr>
                <tr>
                        <td><code>mypass view -r/ref [reference] --show</code></td>
                        <td>Display full detail of the data and decrypt password</td>
                </tr>
                <tr>
                        <td><code>mypass view -a --limit NUMBER</code></td>
                        <td>Total number of data to be display. (default: 3)</td>
                </tr>
                <tr>
                        <td><code>mypass view -a --offset NUMBER</code></td>
                        <td>Starting number of data to be display. (default: 0)</td>
                </tr>
                <tr>
                        <td><code>mypass view -a --limit 4 --offset 1</code></td>
                        <td>Display only 4 data startin from 1</td>
                </tr>
                <tr>
                        <td><code>mypass view -h</code></td>
                        <td>Display <code>view</code> help options</td>
                </tr>
                <tr>
                        <td><code>mypass search -u KEYWORD</code></td>
                        <td>Filter data by username based on provided keyword</td>
                </tr>
                <tr>
                        <td><code>mypass search -n KEYWORD</code></td>
                        <td>Filter data by name based on provided keyword</td>
                </tr>
                <tr>
                        <td><code>mypass search -p KEYWORD</code></td>
                        <td>Filter data by password based on provided keyword</td>
                </tr>
                <tr>
                        <td><code>mypass search -u KEYWORD -n KEYWORD</code></td>
                        <td>Filter data by username and name based on provided keyword</td>
                </tr>
                <tr>
                        <td><code>mypass search -u KEYWORD --limit NUMBER</code></td>
                        <td>Total number of data to be display. (default: 3)</td>
                </tr>
                <tr>
                        <td><code>mypass search -u KEYWORD --offset NUMBER</code></td>
                        <td>Starting number of data to be display. (default: 0)</td>
                </tr>
                <tr>
                        <td><code>mypass search -h</code></td>
                        <td>Display <code>search</code> help option.</td>
                </tr>
                <tr>
                        <td><code>mypass rmv -r/--ref REFERENCE</code></td>
                        <td>Remove REFERENCE.</td>
                </tr>
                <tr>
                        <td><code>mypass rmv -a/--all</code></td>
                        <td>Remove all data.</td>
                </tr>
                <tr>
                        <td><code>mypass rmv -h</code></td>
                        <td>Display remove help option.</td>
                </tr>
        </tbody>
</table>
