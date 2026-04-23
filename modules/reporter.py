def generate_summary(findings_list):

    total_risks = len(findings_list)

    severity_count = {"critial" : 0, "high" : 0, "medium" : 0, "low" : 0,}
    issue_count = {}
    action_items = []
    
    for finding in findings_list:
        severity = finding.get("severity", "").lower()
        issue = finding.get("issue", "Unknown Issue")
        rule_id = finding.get("rule_id", "Unknown")
        
        if severity in severity_count:
            severity_count[severity] += 1

        if issue in issue_count:
            issue_count[issue] += 1
        else:
            issue_count[issue] = 1

        if severity == "high" or severity == "critical":
            if rule_id not in action_items:
                action_items.append(rule_id)
            
    high_critical_total = severity_count["high"] + severity_count["critial"]

    if high_critical_total > 0:
        system_status = "DANGER"
    elif severity_count["medium"] > 0:
        system_status = "WARNING"
    else:
        system_status = "SECURE"

    review_output = {
        'total_risks': total_risks,
        'status': system_status,
        'severity_count': severity_count,
        'common_issues': issue_count,
        'rule_needing_action': action_items
    }

    return review_output

# testing part, run 'python reporter.py' on terminal, make sure nakapasok din sa modules folder (cd modules)
if __name__ == "__main__":

    import json

    sample_analyzer = [
        {"rule_id": 4, "severity": "High", "issue": "Insecure Port Allowed", "message": "Port 23 is openly permitted."},
        {"rule_id": 2, "severity": "Medium", "issue": "Wide Source Exposure", "message": "Source is set to 'any'."},
        {"rule_id": 8, "severity": "High", "issue": "Insecure Port Allowed", "message": "Port 445 is openly permitted."},
        {"rule_id": 10, "severity": "Low", "issue": "Unnecessary Rule", "message": "Rule is redundant."}
    ]
    
    review_output = generate_summary(sample_analyzer)

    print("")
    print("Final Output:")
    print(json.dumps(review_output, indent=4))