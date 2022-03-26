// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract PaySalaries is Ownable {
    // kept value for gas fees
    uint256 keptValue = 3000000000000000000;
    // get salary of an employee
    mapping(address => uint256) public EmployeeSalary;
    // get a salary of an occupation
    mapping(string => uint256) public OccupationSalary;
    // array of employees must be payable
    address[] public employees;
    // array of occupations
    string[] public occupations;
    // last paiments
    uint256 public lastTransfeers;
    

    //events
    event EmployeeAddedSuccefully(
        address employee,
        string occupation,
        uint256 salary
    );
    event OccupationAddedSuccefully(string occupationName);
    event BalanceAddedSuccefully(
        uint256 amountAdded,
        uint256 currentBalance,
        address sender
    );
    event OccupationSalaryUpdatedSuccefully(uint256 salary, string occupation);
    event SalarySentSuccefully(uint256 salary, address employee, uint256 time);

    constructor ()  {
        lastTransfeers = block.timestamp;
    }

    // add balance to the contract

    function fundWithEth() public payable {
        emit BalanceAddedSuccefully(msg.value,address(this).balance,msg.sender);
    }

    // return contract balance

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    // add employee and his occupation post
    function addEmployee(address _employee, string memory _occupation)
        public
        onlyOwner
    {
        // the employee should donesn't exist before in our employees
        require(
            checkEmployeeIfExist(_employee) == false,
            "employee already exist "
        );
        // the occupation must be exist in occupations
        require(
            checkOccupationIfExist(_occupation) == true,
            "occupation doesn't exist "
        );
        // the occupation salary must be great than 0 
        require(
            OccupationSalary[_occupation] > 0,
            "This occupation deosn't have price"
        );
        employees.push(_employee);
        EmployeeSalary[_employee] = OccupationSalary[_occupation];
        emit EmployeeAddedSuccefully(
            _employee,
            _occupation,
            EmployeeSalary[_employee]
        );
    }

    // add an occupation

    function addOccupation(string memory _occupation) public onlyOwner {
        require(
            checkOccupationIfExist(_occupation) == false,
            "Occupation already exist"
        );
        occupations.push(_occupation);
        emit OccupationAddedSuccefully(_occupation);
    }

    // add / modify an occupation salary

    function addOrModifyOccupationSalary(
        string memory _occupation,
        uint256 _salary
    ) public onlyOwner {
        require(
            checkOccupationIfExist(_occupation) == true,
            "Occupation deosn't exist"
        );
        OccupationSalary[_occupation] = _salary;
        emit OccupationSalaryUpdatedSuccefully(_salary, _occupation);
    }

    // return true if the employee exist, else return false
    function checkEmployeeIfExist(address _employee)
        public
        view
        returns (bool)
    {
        for (uint256 i = 0; i < employees.length; i++) {
            if (employees[i] == _employee) {
                return true;
            }
        }
        return false;
    }

    // return true if occupation exist, else return false

    function checkOccupationIfExist(string memory _occupation)
        public
        view
        returns (bool)
    {
        for (uint256 i = 0; i < occupations.length; i++) {
            // compare two strings
            if (
                keccak256(abi.encodePacked((occupations[i]))) ==
                keccak256(abi.encodePacked((_occupation)))
            ) {
                return true;
            }
        }
        return false;
    }

    // the main functionallity strart from here

    // sending to all user salary every 30 days

    function transferSalaries() public onlyOwner {
        require(block.timestamp > lastTransfeers + 30 seconds, "You need to wait more");
        // the contract balance must be enough to pay all the employees
        require(
            totalSalariesMustBePaied() < address(this).balance + keptValue,
            "Balance not enough"
        );
        for (uint256 i = 0; i < employees.length; i++) {
            address recipient = employees[i];
            (bool sent, ) = payable(recipient).call{
                value: EmployeeSalary[recipient]
            }("");
            require(sent, "failed to send eth");
            emit SalarySentSuccefully(
                EmployeeSalary[recipient],
                recipient,
                block.timestamp
            );
        }
        lastTransfeers = block.timestamp;
    }

    // return true if balance enough else return false

    function totalSalariesMustBePaied() public view returns (uint256) {
        uint256 totalSalaries = 0;
        for (uint256 i = 0; i < employees.length; i++) {
            totalSalaries += EmployeeSalary[employees[i]];
        }
        return totalSalaries;
    }

    // function maybe useful under developement to get your eth back from the contract

    function backDoor() public onlyOwner {
        address recepient = owner();
        (bool sent, ) = payable(recepient).call{value: address(this).balance}("");
        require(sent, "failed to sent eth");
    }
}
